from typing import Annotated

from common.logger import get_logger
from fastapi import APIRouter, HTTPException, Query
from schemas import ChannelMessagesResponse
from services.http.telegram import fetch_detailed_message, fetch_newest_message_id


__all__ = ["router"]

logger = get_logger(__name__)

router = APIRouter()


@router.get("/channel/{channel_username}/messages")
async def channel_messages(
    channel_username: str, last_message_id: Annotated[int | None, Query()] = None
) -> ChannelMessagesResponse:
    newest_message_id = await fetch_newest_message_id(channel_username)
    if newest_message_id is None:
        return ChannelMessagesResponse(messages=[])

    if last_message_id is None:
        # Парсим offset_last_message последних сообщений для актуализации вакансий
        offset_last_message = 100
        last_message_id = newest_message_id - offset_last_message
        logger.info("Last message id is unknown, using %s", last_message_id)

    max_messages_interval = 300
    if (newest_message_id - last_message_id) > max_messages_interval:
        msg = f"Messages interval great then {max_messages_interval}. Increase last_message_id if possible"
        raise HTTPException(status_code=500, detail=msg)

    # +1 т.к. не нужно парсить уже известное сообщение и идем включительно до последнего сообщения
    message_ids_to_parse = list(range(last_message_id, newest_message_id + 1))
    messages = await fetch_detailed_message(channel_username, message_ids_to_parse)

    return ChannelMessagesResponse(messages=messages)
