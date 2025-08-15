from datetime import datetime

from pydantic import BaseModel


__all__ = [
    "ProfessionResponse",
    "ProfessionSchema",
    "TelegramChannelMessageSchema",
    "TelegramChannelMessagesResponse",
    "TelegramNewestMessagesRequest",
]


class ProfessionSchema(BaseModel):
    id: int
    name: str


class ProfessionResponse(BaseModel):
    professions: list[ProfessionSchema]


class TelegramNewestMessagesRequest(BaseModel):
    after_message_id: int | None


class TelegramChannelMessageSchema(BaseModel):
    id: int
    datetime: datetime
    text: str


class TelegramChannelMessagesResponse(BaseModel):
    messages: list[TelegramChannelMessageSchema]
