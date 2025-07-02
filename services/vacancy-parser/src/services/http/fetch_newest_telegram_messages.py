from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.logger import get_logger
from httpx import AsyncClient
from schemas import TelegramChannelMessage, TelegramChannelMessagesResponse


__all__ = ["fetch_newest_telegram_messages"]


logger = get_logger(__name__)


async def fetch_newest_telegram_messages(
    channel_username: str, last_message_id: int | None = None
) -> list[TelegramChannelMessage]:
    """Возвращает список актуальных сообщений относительно переданного last_message_id"""
    logger.debug("Getting messages from telegram api services")

    url = build_service_url(ServiceEnum.TELEGRAM_API, f"/api/v1/channel/{channel_username}/messages")

    params = {}
    if last_message_id is not None:
        params["last_message_id"] = last_message_id

    async with AsyncClient(timeout=10) as client:
        response = await client.get(str(url), params=params)
        response.raise_for_status()

    data = TelegramChannelMessagesResponse(**response.json())

    return data.messages
