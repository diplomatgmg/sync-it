from database.models.enums import GradeEnum
from pydantic import BaseModel, ConfigDict


__all__ = ["GradeCreate", "GradeRead"]


class BaseGrade(BaseModel):
    name: GradeEnum


class GradeCreate(BaseGrade):
    pass


class GradeRead(BaseGrade):
    id: int

    model_config = ConfigDict(from_attributes=True)
