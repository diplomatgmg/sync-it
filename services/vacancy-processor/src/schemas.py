from pydantic import BaseModel


__all__ = [
    "CompletionResponse",
    "VacancyDeleteResponse",
    "VacancyResponse",
    "VacancySchema",
]


class VacancySchema(BaseModel):
    hash: str
    link: str
    data: str


class VacancyResponse(BaseModel):
    vacancies: list[VacancySchema]


class VacancyDeleteResponse(BaseModel):
    is_deleted: bool


class CompletionResponse(BaseModel):
    message: str
