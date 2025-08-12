from database.models.enums import ProfessionEnum
from pydantic import BaseModel, ConfigDict


__all__ = ["ProfessionCreate", "ProfessionRead"]


class BaseProfession(BaseModel):
    name: ProfessionEnum


class ProfessionCreate(BaseProfession):
    pass


class ProfessionRead(BaseProfession):
    id: int

    model_config = ConfigDict(from_attributes=True)
