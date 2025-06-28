from pydantic import BaseModel


__all__ = [
    "CompletionResponse",
    "VacancyResponse",
    "VacancySchema",
]


class VacancySchema(BaseModel):
    hash: str
    link: str
    data: str


class VacancyResponse(BaseModel):
    vacancies: list[VacancySchema]


class CompletionResponse(BaseModel):
    message: str
