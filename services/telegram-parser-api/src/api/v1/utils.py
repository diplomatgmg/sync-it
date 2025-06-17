import asyncio

from bs4 import BeautifulSoup
import httpx
from schemas import ChannelMessage

from libs.logger import get_logger


__all__ = ["get_messages_by_ids", "get_newest_message_id"]


logger = get_logger(__name__)


async def get_newest_message_id(channel_username: str) -> int | None:
    """Возвращает ID самого последнего (новейшего) сообщения из публичного канала."""
    channel_url = f"https://t.me/s/{channel_username}"

    async with httpx.AsyncClient() as client:
        response = await client.get(channel_url)

        # Если это группа, канал закрыт или его не существует
        if response.is_redirect:
            logger.info("Channel %s is not public or does not exist")
            return None

        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    last_message_widget = soup.select("div.tgme_widget_message")[-1]
    data_post = last_message_widget.attrs.get("data-post")

    newest_message_id = int(data_post.split("/")[-1])
    logger.debug("Newest message id is %s", newest_message_id)

    return newest_message_id


MAX_CONCURRENT_REQUESTS = 50
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def fetch_message(client: httpx.AsyncClient, channel_username: str, message_id: int) -> ChannelMessage | None:
    """Возвращает id и текст сообщений по переданным id."""
    async with semaphore:
        try:
            logger.debug("Getting message with id %s", message_id)
            response = await client.get(f"https://t.me/s/{channel_username}/{message_id}?before={message_id + 1}")
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            data_post_value = f"{channel_username}/{message_id}"
            message_block = soup.find("div", class_="tgme_widget_message", attrs={"data-post": data_post_value})

            if message_block is None:
                logger.debug("Message block not found for message with id %s", message_id)
                return None

            message_text_block = soup.select_one("div.tgme_widget_message_text")
            if message_text_block is None:
                logger.debug("Message text block not found for message with id %s", message_id)
                return None

            for br in message_text_block.find_all("br"):
                br.replace_with("\n")

            return ChannelMessage(
                message_id=message_id,
                text=message_text_block.get_text().strip(),
            )
        except Exception as e:
            logger.exception("Error fetching message with id %s", message_id, exc_info=e)
            return None


async def get_messages_by_ids(channel_username: str, message_ids: list[int]) -> list[ChannelMessage]:
    logger.debug("Getting messages by ids %s", message_ids)

    client_limits = httpx.Limits(
        max_connections=MAX_CONCURRENT_REQUESTS, max_keepalive_connections=MAX_CONCURRENT_REQUESTS
    )
    async with httpx.AsyncClient(limits=client_limits) as client:
        tasks = [fetch_message(client, channel_username, message_id) for message_id in message_ids]
        results = await asyncio.gather(*tasks)

    return [msg for msg in results if msg is not None]
