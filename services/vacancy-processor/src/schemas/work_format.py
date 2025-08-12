from database.models.enums import WorkFormatEnum
from pydantic import BaseModel, ConfigDict


__all__ = ["WorkFormatCreate", "WorkFormatRead"]


class BaseWorkFormat(BaseModel):
    name: WorkFormatEnum


class WorkFormatCreate(BaseWorkFormat):
    pass


class WorkFormatRead(BaseWorkFormat):
    id: int

    model_config = ConfigDict(from_attributes=True)
