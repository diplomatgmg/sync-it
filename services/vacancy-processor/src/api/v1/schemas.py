from pydantic import BaseModel
from schemas.grade import GradeRead
from schemas.profession import ProfessionRead
from schemas.skill import SkillCategoryRead, SkillRead
from schemas.work_format import WorkFormatRead


__all__ = [
    "GradeListResponse",
    "ProfessionListResponse",
    "WorkFormatListResponse",
]


class ProfessionListResponse(BaseModel):
    professions: list[ProfessionRead]


class GradeListResponse(BaseModel):
    grades: list[GradeRead]


class WorkFormatListResponse(BaseModel):
    work_formats: list[WorkFormatRead]


class SkillCategoryListResponse(BaseModel):
    skill_categories: list[SkillCategoryRead]


class SkillListResponse(BaseModel):
    skills: list[SkillRead]
