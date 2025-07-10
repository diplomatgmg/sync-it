from pydantic import BaseModel


__all__ = [
    "Grade",
    "GradeResponse",
    "Profession",
    "ProfessionResponse",
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
