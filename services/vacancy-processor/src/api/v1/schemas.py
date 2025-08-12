from pydantic import BaseModel
from schemas.grade import GradeRead
from schemas.profession import ProfessionRead


__all__ = [
    "ProfessionListResponse",
]


class ProfessionListResponse(BaseModel):
    professions: list[ProfessionRead]


class GradeListResponse(BaseModel):
    grades: list[GradeRead]
