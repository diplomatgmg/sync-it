from pydantic import BaseModel


__all__ = [
    "TelegramDetailedMessageParams",
    "TelegramPingResponse",
]


class TelegramPingResponse(BaseModel):
    status: str = "pong"


class TelegramDetailedMessageParams(BaseModel):
    before: int
