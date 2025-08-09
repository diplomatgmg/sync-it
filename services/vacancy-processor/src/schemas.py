from datetime import datetime

from pydantic import BaseModel, ConfigDict


__all__ = [
    "CompletionResponse",
    "GradeModelResponse",
    "GradeModelSchema",
    "HealthResponse",
    "ParsedVacancyDeleteResponse",
    "ParsedVacancyResponse",
    "ParsedVacancySchema",
    "ProcessedVacancyModelSchema",
    "ProfessionModelResponse",
    "ProfessionModelSchema",
    "SkillCategoryModelResponse",
    "SkillCategoryModelSchema",
    "SkillModelResponse",
    "SkillModelSchema",
    "VacancyModelResponse",
    "WorkFormatModelResponse",
    "WorkFormatModelSchema",
]


class ParsedVacancySchema(BaseModel):
    hash: str
    link: str
    data: str
    published_at: datetime


class ParsedVacancyResponse(BaseModel):
    vacancies: list[ParsedVacancySchema]


class ParsedVacancyDeleteResponse(BaseModel):
    is_deleted: bool


class CompletionResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str


class SkillModelSchema(BaseModel):
    id: int
    category_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SkillModelResponse(BaseModel):
    skills: list[SkillModelSchema]


class SkillCategoryModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SkillCategoryModelResponse(BaseModel):
    categories: list[SkillCategoryModelSchema]


class GradeModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class GradeModelResponse(BaseModel):
    grades: list[GradeModelSchema]


class ProfessionModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProfessionModelResponse(BaseModel):
    professions: list[ProfessionModelSchema]


class WorkFormatModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class WorkFormatModelResponse(BaseModel):
    work_formats: list[WorkFormatModelSchema]


class ProcessedVacancyModelSchema(BaseModel):
    id: int
    link: str
    published_at: datetime
    company_name: str | None
    profession: ProfessionModelSchema | None
    grades: list[GradeModelSchema]
    work_formats: list[WorkFormatModelSchema]
    workplace_description: str | None
    responsibilities: str | None
    requirements: str | None
    conditions: str | None

    model_config = ConfigDict(from_attributes=True)


class VacancyModelResponse(BaseModel):
    vacancies: list[ProcessedVacancyModelSchema]
