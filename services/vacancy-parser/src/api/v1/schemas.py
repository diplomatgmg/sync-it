from pydantic import BaseModel
from schemas.vacancy import BaseVacancyRead


__all__ = [
    "VacancyDeleteResponse",
    "VacancyListResponse",
]


class VacancyListResponse(BaseModel):
    vacancies: list[BaseVacancyRead]


class VacancyDeleteResponse(BaseModel):
    is_deleted: bool
