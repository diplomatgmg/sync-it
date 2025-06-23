from pydantic import BaseModel, ConfigDict


__all__ = ["VacancySerializer"]


class VacancySerializer(BaseModel):
    hash: str
    link: str
    data: str

    model_config = ConfigDict(from_attributes=True)
