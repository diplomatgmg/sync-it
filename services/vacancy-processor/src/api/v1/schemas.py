from pydantic import BaseModel
from schemas.profession import ProfessionRead


__all__ = [
    "ProfessionListResponse",
]


class ProfessionListResponse(BaseModel):
    professions: list[ProfessionRead]
