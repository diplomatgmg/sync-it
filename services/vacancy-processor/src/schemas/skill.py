from database.models.enums import SkillEnum
from pydantic import BaseModel, ConfigDict


__all__ = [
    "SkillCreate",
    "SkillRead",
]


class BaseSkill(BaseModel):
    name: SkillEnum


class SkillCreate(BaseSkill):
    pass


class SkillRead(BaseSkill):
    id: int

    model_config = ConfigDict(from_attributes=True)
