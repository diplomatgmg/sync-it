from datetime import datetime

from common.shared.schemas import HttpsUrl
from database.models.enums import SourceEnum
from pydantic import BaseModel


__all__ = [
    "CompletionResponse",
    "VacancyDeleteResponse",
    "VacancyResponse",
    "VacancySchema",
]


class CompletionResponse(BaseModel):
    message: str


class VacancySchema(BaseModel):
    id: int
    source: SourceEnum
    hash: str
    link: HttpsUrl
    data: str
    published_at: datetime


class VacancyResponse(BaseModel):
    vacancies: list[VacancySchema]


class VacancyDeleteResponse(BaseModel):
    is_deleted: bool
