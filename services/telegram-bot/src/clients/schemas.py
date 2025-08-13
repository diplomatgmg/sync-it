from datetime import datetime

from pydantic import BaseModel


__all__ = [
    "GradeResponse",
    "GradeSchema",
    "ProfessionResponse",
    "ProfessionSchema",
    "SkillCategoryResponse",
    "SkillCategorySchema",
    "SkillResponse",
    "SkillSchema",
    "VacancyWithNeighborsRequest",
    "VacancyWithNeighborsResponse",
    "VacancyWithNeighborsSchema",
    "WorkFormatResponse",
    "WorkFormatSchema",
]


class GradeSchema(BaseModel):
    id: int
    name: str


class GradeResponse(BaseModel):
    grades: list[GradeSchema]


class ProfessionSchema(BaseModel):
    id: int
    name: str


class ProfessionResponse(BaseModel):
    professions: list[ProfessionSchema]


class WorkFormatSchema(BaseModel):
    id: int
    name: str


class WorkFormatResponse(BaseModel):
    work_formats: list[WorkFormatSchema]


class SkillCategorySchema(BaseModel):
    id: int
    name: str


class SkillCategoryResponse(BaseModel):
    skill_categories: list[SkillCategorySchema]


class SkillSchema(BaseModel):
    id: int
    category_id: int
    name: str


class SkillResponse(BaseModel):
    skills: list[SkillSchema]


class VacancySchema(BaseModel):
    id: int
    hash: str
    link: str
    company_name: str | None
    salary: str | None
    profession: ProfessionSchema | None
    skills: list[SkillSchema]
    grades: list[GradeSchema]
    work_formats: list[WorkFormatSchema]
    workplace_description: str | None
    responsibilities: str | None
    requirements: str | None
    conditions: str | None
    published_at: datetime


class VacancyWithNeighborsSchema(BaseModel):
    prev_id: int | None
    next_id: int | None
    vacancy: VacancySchema | None


class VacancyWithNeighborsRequest(BaseModel):
    professions: list[str] | None = None
    grades: list[str] | None = None
    work_formats: list[str] | None = None
    skills: list[str] | None = None


class VacancyWithNeighborsResponse(BaseModel):
    result: VacancyWithNeighborsSchema
