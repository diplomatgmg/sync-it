from datetime import datetime
from enum import StrEnum

from common.logger import get_logger
from common.shared.schemas import HttpsUrl
from pydantic import BaseModel


__all__ = [
    "GradeResponse",
    "GradeSchema",
    "ProfessionResponse",
    "ProfessionSchema",
    "SkillResponse",
    "SkillSchema",
    "VacancyWithNeighborsRequest",
    "VacancyWithNeighborsResponse",
    "VacancyWithNeighborsSchema",
    "WorkFormatResponse",
    "WorkFormatSchema",
]


logger = get_logger(__name__)


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


class SkillSchema(BaseModel):
    id: int
    name: str


class SkillResponse(BaseModel):
    skills: list[SkillSchema]


class SourceEnum(StrEnum):
    TELEGRAM = "telegram"
    HEAD_HUNTER = "head_hunter"

    def humanize(self) -> str:
        if self == SourceEnum.TELEGRAM:
            return "Telegram"
        if self == SourceEnum.HEAD_HUNTER:
            return "HeadHunter"

        logger.error("Unknown source: %s", self)
        return "Неизвестно"


class VacancySchema(BaseModel):
    id: int
    source: SourceEnum
    hash: str
    link: HttpsUrl
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
