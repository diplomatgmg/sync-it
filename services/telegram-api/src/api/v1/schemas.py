from pydantic import BaseModel
from schemas import ChannelMessageSchema


__all__ = ["ChannelMessagesResponse"]


class ChannelMessagesResponse(BaseModel):
    messages: list[ChannelMessageSchema]
