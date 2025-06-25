import asyncio

from bs4 import BeautifulSoup
from common.logger import get_logger
import httpx
from schemas import ChannelMessage


__all__ = [
    "get_messages_by_ids",
    "get_newest_message_id",
]


logger = get_logger(__name__)


MAX_CONCURRENT_REQUESTS = 50
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


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
    data_post = last_message_widget.attrs["data-post"]

    newest_message_id = int(str(data_post).split("/")[-1])
    logger.debug("Newest message id is %s", newest_message_id)

    return newest_message_id


async def get_messages_by_ids(channel_username: str, message_ids: list[int]) -> list[ChannelMessage]:
    """Возвращает текст и id сообщений по переданным id."""
    logger.debug("Getting messages by ids %s", message_ids)

    client_limits = httpx.Limits(
        max_connections=MAX_CONCURRENT_REQUESTS, max_keepalive_connections=MAX_CONCURRENT_REQUESTS
    )
    async with httpx.AsyncClient(limits=client_limits) as client:
        tasks = [_fetch_message(client, channel_username, message_id) for message_id in message_ids]
        results = await asyncio.gather(*tasks)

    return [msg for msg in results if msg is not None]


async def _fetch_message(client: httpx.AsyncClient, channel_username: str, message_id: int) -> ChannelMessage | None:
    """Парсит сообщение по id."""
    async with semaphore:
        try:
            logger.debug("Getting message with id %s", message_id)
            response = await client.get(f"https://t.me/s/{channel_username}/{message_id}?before={message_id + 1}")
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            data_post_value = f"{channel_username}/{message_id}"
            message_block = soup.select_one(f'div.tgme_widget_message[data-post="{data_post_value}"]')

            if message_block is None:
                # Если сообщение удалено
                logger.debug("Message with id %s was deleted", message_id)
                return None

            data_post = message_block.attrs.get("data-post")
            if data_post != data_post_value:
                logger.error(
                    "Data-post value mismatch for message with id %s. Expected %s, got %s",
                    message_id,
                    data_post_value,
                    data_post,
                )
                return None

            is_not_supported_message = message_block.select_one("div.message_media_not_supported")
            # Сообщение не поддерживается: Please open Telegram to view this post
            if is_not_supported_message is not None:
                logger.debug("Message with id %s is not supported", message_id)
                return None

            message_text_block = message_block.select_one("div.tgme_widget_message_text")
            # Если в сообщении нет текста (Только картинки, видео, документы и т.д.)
            if message_text_block is None:
                logger.debug("Message text block not found for message with id %s", message_id)
                return None

            for br in message_text_block.find_all("br"):
                br.replace_with("\n")  # type: ignore[arg-type]

            return ChannelMessage(
                message_id=message_id,
                text=message_text_block.get_text().strip(),
            )
        except Exception as e:
            logger.exception("Error fetching message with id %s", message_id, exc_info=e)
            return None
