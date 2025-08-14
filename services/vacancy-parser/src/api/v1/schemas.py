from pydantic import BaseModel, Field
from schemas.vacancy import VacancyRead


__all__ = [
    "VacancyDeleteResponse",
    "VacancyListResponse",
]


class VacancySchema(VacancyRead):
    fingerprint: str = Field(exclude=True)


class VacancyListResponse(BaseModel):
    vacancies: list[VacancySchema]


class VacancyDeleteResponse(BaseModel):
    is_deleted: bool
