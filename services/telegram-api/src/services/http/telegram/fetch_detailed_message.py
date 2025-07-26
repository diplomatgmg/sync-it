import asyncio

from bs4 import BeautifulSoup
from common.logger import get_logger
from httpx import AsyncClient, Limits
from schemas import ChannelMessage


__all__ = ["fetch_detailed_message"]


logger = get_logger(__name__)


MAX_CONCURRENT_REQUESTS = 50

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
client_limits = Limits(
    max_connections=MAX_CONCURRENT_REQUESTS,
    max_keepalive_connections=MAX_CONCURRENT_REQUESTS,
)


async def fetch_detailed_message(channel_username: str, message_ids: list[int]) -> list[ChannelMessage]:
    """Возвращает текст и id сообщений по переданным id."""
    logger.debug("Getting messages by ids %s", message_ids)

    async with AsyncClient(limits=client_limits) as client:
        tasks = [_fetch_and_parse_message(client, channel_username, message_id) for message_id in message_ids]
        results = await asyncio.gather(*tasks)

    return [msg for msg in results if msg is not None]


async def _fetch_and_parse_message(  # noqa: PLR0911 Too many return statements
    client: AsyncClient, channel_username: str, message_id: int
) -> ChannelMessage | None:
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
                logger.info("Message with id %s was deleted", message_id)
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
                logger.info("Message with id %s is not supported", message_id)
                return None

            message_text_block = message_block.select_one("div.tgme_widget_message_text")
            # Если в сообщении нет текста (Только картинки, видео, документы и т.д.)
            if message_text_block is None:
                logger.info("Message text block not found for message with id %s", message_id)
                return None

            message_time_block = message_block.select_one("time.time")
            if message_time_block is None:
                logger.warning("Message time not found for message with id %s", message_id)
                return None

            message_datetime_str = str(message_time_block.attrs["datetime"])

            for br in message_text_block.find_all("br"):
                br.replace_with("\n")  # type: ignore[arg-type]

            return ChannelMessage(
                id=message_id,
                datetime=message_datetime_str,
                text=message_text_block.get_text().strip(),
            )
        except Exception as e:
            logger.exception("Error fetching message with id %s", message_id, exc_info=e)
            return None
