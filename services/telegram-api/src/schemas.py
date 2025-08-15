from pydantic import BaseModel


__all__ = ["ChannelMessageSchema"]


class ChannelMessageSchema(BaseModel):
    id: int
    datetime: str
    text: str
