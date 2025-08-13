from database.models.enums import SourceEnum
from pydantic import BaseModel, ConfigDict


__all__ = [
    "SourceCreate",
    "SourceRead",
]


class SourceBase(BaseModel):
    name: SourceEnum


class SourceCreate(SourceBase):
    pass


class SourceRead(SourceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
