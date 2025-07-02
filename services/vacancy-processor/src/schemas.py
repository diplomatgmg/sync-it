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
    "VacancyListResponse",
    "VacancyModelSchema",
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


class VacancyModelSchema(BaseModel):
    id: int
    link: str
    profession: ProfessionModelSchema | None
    grades: list[GradeModelSchema]
    work_formats: list[WorkFormatModelSchema]

    model_config = ConfigDict(from_attributes=True)


# FIXME
# У меня уже есть VacancyResponse. Надо придумать, как назвать ответы моделей (как ниже)
# И ответы со стороны api
class VacancyListResponse(BaseModel):
    vacancies: list[VacancyModelSchema]

    # FIXME мб сделать метод from_orm? Например, вынести schemas > models, orm (тут будет baseOrmSchema)
    # @classmethod
    # def from_orm_list(cls, vacancies: list):
    #     return cls(vacancies=[VacancySchema.from_orm(v) for v in vacancies])  # noqa: ERA001
