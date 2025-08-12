from database.models.enums import SkillCategoryEnum, SkillEnum
from pydantic import BaseModel, ConfigDict


__all__ = [
    "SkillCategoryCreate",
    "SkillCategoryRead",
    "SkillCreate",
    "SkillRead",
]


class BaseSkillCategory(BaseModel):
    name: SkillCategoryEnum


class SkillCategoryCreate(BaseSkillCategory):
    pass


class SkillCategoryRead(BaseSkillCategory):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BaseSkill(BaseModel):
    name: SkillEnum
    category_id: int


class SkillCreate(BaseSkill):
    pass


class SkillRead(BaseSkill):
    id: int

    model_config = ConfigDict(from_attributes=True)
