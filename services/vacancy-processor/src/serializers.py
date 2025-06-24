from pydantic import BaseModel


__all__ = ["VacancySerializer"]


class VacancySerializer(BaseModel):
    hash: str
    link: str
    data: str
