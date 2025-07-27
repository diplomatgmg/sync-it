from datetime import datetime

from pydantic import BaseModel


__all__ = [
    "Grade",
    "GradeResponse",
    "Profession",
    "ProfessionResponse",
    "Vacancy",
    "VacancyRequest",
    "VacancyResponse",
    "WorkFormat",
    "WorkFormatResponse",
]


class Profession(BaseModel):
    id: int
    name: str


class ProfessionResponse(BaseModel):
    professions: list[Profession]


class Grade(BaseModel):
    id: int
    name: str


class GradeResponse(BaseModel):
    grades: list[Grade]


class WorkFormat(BaseModel):
    id: int
    name: str


class WorkFormatResponse(BaseModel):
    work_formats: list[WorkFormat]


class VacancyRequest(BaseModel):
    professions: list[str] | None = None
    grades: list[str] | None = None
    work_formats: list[str] | None = None


class Vacancy(BaseModel):
    id: int
    link: str
    published_at: datetime
    profession: Profession | None
    grades: list[Grade]
    work_formats: list[WorkFormat]
    workplace_description: str | None
    responsibilities: str | None
    requirements: str | None
    conditions: str | None


class VacancyResponse(BaseModel):
    vacancies: list[Vacancy]
