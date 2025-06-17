from pydantic import BaseModel


__all__ = [
    "ChannelMessage",
    "ChannelMessagesResponse",
    "HealthResponse",
]


class HealthResponse(BaseModel):
    status: str


class ChannelMessage(BaseModel):
    message_id: int
    text: str


class ChannelMessagesResponse(BaseModel):
    messages: list[ChannelMessage]
