from pydantic import BaseModel
from serializers import VacancySerializer


__all__ = [
    "CompletionResponse",
    "VacancyResponse",
]


class VacancyResponse(BaseModel):
    vacancies: list[VacancySerializer]


class CompletionResponse(BaseModel):
    message: str
