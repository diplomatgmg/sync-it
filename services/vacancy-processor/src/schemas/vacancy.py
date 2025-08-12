from datetime import datetime

from pydantic import BaseModel, ConfigDict


__all__ = [
    "VacancyCreate",
    "VacancyRead",
]


class BaseVacancy(BaseModel):
    hash: str
    link: str

    profession_id: int
    company_name: str | None
    salary: str | None
    workplace_description: str | None
    responsibilities: str | None
    requirements: str | None
    conditions: str | None

    published_at: datetime


class VacancyCreate(BaseVacancy):
    pass


class VacancyRead(BaseVacancy):
    id: int

    model_config = ConfigDict(from_attributes=True)
