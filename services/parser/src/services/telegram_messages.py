import httpx


__all__ = ["get_newest_telegram_messages"]

from libs.logger import get_logger
from schemas import TelegramChannelMessage
from schemas import TelegramChannelMessagesResponse


logger = get_logger(__name__)


async def get_newest_telegram_messages(
        channel_username: str,
        last_message_id: int | None = None
) -> list[TelegramChannelMessage]:
    """Возвращает список актуальных сообщений относительно переданного last_message_id"""
    logger.debug("Getting messages from telegram api services")

    url = f"http://telegram-parser-api:8001/api/v1/channel/{channel_username}/messages"  # FIXME hardcore

    params = {}
    if last_message_id is not None:
        params["last_message_id"] = last_message_id

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()

    data = TelegramChannelMessagesResponse(**response.json())
    messages = data.messages

    logger.info("Got %s new messages", len(messages))

    return messages
