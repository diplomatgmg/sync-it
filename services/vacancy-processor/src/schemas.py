from pydantic import BaseModel, ConfigDict


__all__ = [
    "CompletionResponse",
    "GradeModelSchema",
    "GradeResponse",
    "HealthResponse",
    "ProfessionModelSchema",
    "ProfessionResponse",
    "SkillCategoryModelSchema",
    "SkillCategoryResponse",
    "SkillModelSchema",
    "SkillResponse",
    "VacancyDeleteResponse",
    "VacancyResponse",
    "VacancySchema",
    "WorkFormatModelSchema",
    "WorkFormatResponse",
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


class HealthResponse(BaseModel):
    status: str


class SkillModelSchema(BaseModel):
    id: int
    category_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SkillResponse(BaseModel):
    skills: list[SkillModelSchema]


class SkillCategoryModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SkillCategoryResponse(BaseModel):
    categories: list[SkillCategoryModelSchema]


class GradeModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class GradeResponse(BaseModel):
    grades: list[GradeModelSchema]


class ProfessionModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProfessionResponse(BaseModel):
    professions: list[ProfessionModelSchema]


class WorkFormatModelSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class WorkFormatResponse(BaseModel):
    work_formats: list[WorkFormatModelSchema]
