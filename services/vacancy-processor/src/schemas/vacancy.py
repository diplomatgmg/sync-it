from datetime import datetime

from pydantic import BaseModel, ConfigDict
from schemas.grade import GradeRead
from schemas.profession import ProfessionRead
from schemas.skill import SkillRead
from schemas.work_format import WorkFormatRead


__all__ = [
    "VacancyCreate",
    "VacancyRead",
]


class BaseVacancy(BaseModel):
    hash: str
    link: str

    company_name: str | None
    salary: str | None
    workplace_description: str | None
    responsibilities: str | None
    requirements: str | None
    conditions: str | None

    published_at: datetime


class VacancyCreate(BaseVacancy):
    profession_id: int | None


class VacancyRead(BaseVacancy):
    id: int

    profession: ProfessionRead | None
    skills: list[SkillRead]
    grades: list[GradeRead]
    work_formats: list[WorkFormatRead]

    model_config = ConfigDict(from_attributes=True)
