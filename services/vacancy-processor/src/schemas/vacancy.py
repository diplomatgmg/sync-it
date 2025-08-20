from datetime import datetime

from common.shared.schemas import HttpsUrl
from database.models.enums import SourceEnum
from pydantic import BaseModel, ConfigDict, field_serializer, field_validator
from pydantic_core.core_schema import SerializationInfo
from schemas.grade import GradeRead
from schemas.profession import ProfessionRead
from schemas.skill import SkillRead
from schemas.work_format import WorkFormatRead


__all__ = [
    "VacancyCreate",
    "VacancyRead",
]


class BaseVacancy(BaseModel):
    source: SourceEnum
    hash: str
    link: HttpsUrl

    company_name: str | None
    salary: str | None
    workplace_description: str | None
    responsibilities: str | None
    requirements: str | None
    conditions: str | None

    published_at: datetime


class VacancyCreate(BaseVacancy):
    profession_id: int | None

    @field_serializer("link")
    def serialize_link(self, value: HttpsUrl, _info: SerializationInfo) -> str:  # noqa: PLR6301
        return str(value)

    @field_validator("salary")
    @classmethod
    def salary_max_length(cls, value: str | None) -> str | None:
        max_length = 96
        if value is not None and len(value) > max_length:
            raise ValueError("Salary field must not exceed 96 characters")
        return value


class VacancyRead(BaseVacancy):
    id: int

    profession: ProfessionRead | None
    skills: list[SkillRead]
    grades: list[GradeRead]
    work_formats: list[WorkFormatRead]

    model_config = ConfigDict(from_attributes=True)
