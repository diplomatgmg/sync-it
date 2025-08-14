from datetime import datetime

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
    source: str
    hash: str
    link: str
    data: str
    published_at: datetime


class VacancyResponse(BaseModel):
    vacancies: list[VacancySchema]


class VacancyDeleteResponse(BaseModel):
    is_deleted: bool
