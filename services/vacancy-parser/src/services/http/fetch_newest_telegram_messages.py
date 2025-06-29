from common.logger import get_logger
from core.config import service_config
import httpx
from schemas import TelegramChannelMessage, TelegramChannelMessagesResponse


__all__ = ["fetch_newest_telegram_messages"]


logger = get_logger(__name__)


async def fetch_newest_telegram_messages(
    channel_username: str, last_message_id: int | None = None
) -> list[TelegramChannelMessage]:
    """Возвращает список актуальных сообщений относительно переданного last_message_id"""
    logger.debug("Getting messages from telegram api services")

    url = f"{service_config.telegram_api_url}/api/v1/channel/{channel_username}/messages"

    params = {}
    if last_message_id is not None:
        params["last_message_id"] = last_message_id

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()

    data = TelegramChannelMessagesResponse(**response.json())

    return data.messages
