from pydantic import BaseModel
from serializers import VacancySerializer


__all__ = ["VacancyResponse"]


class VacancyResponse(BaseModel):
    vacancies: list[VacancySerializer]
