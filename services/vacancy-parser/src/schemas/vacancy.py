from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field
from utils import generate_hash


__all__ = [
    "BaseVacancyCreate",
    "BaseVacancyRead",
    "HeadHunterVacancyCreate",
    "HeadHunterVacancyRead",
    "TelegramVacancyCreate",
    "TelegramVacancyRead",
    "VacancyRead",
]


class BaseVacancy(BaseModel):
    fingerprint: str
    link: str
    published_at: datetime


class BaseVacancyCreate(BaseVacancy):
    pass


class BaseVacancyRead(BaseVacancy):
    id: int
    hash: str
    source_id: int
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class VacancyRead(BaseVacancyRead, BaseVacancy):
    pass


class BaseHeadHunterVacancy(BaseVacancy):
    vacancy_id: int


class HeadHunterVacancyCreate(BaseVacancyCreate, BaseHeadHunterVacancy):
    employer: str
    name: str
    description: str
    salary: str | None
    experience: str
    employment: str
    schedule: str
    work_formats: list[str]
    key_skills: list[str]

    @property
    @computed_field
    def hash(self) -> str:
        return generate_hash(self.vacancy_id)

    @property
    @computed_field
    def data(self) -> str:
        text_parts: list[str] = [f"Компания: {self.employer}", f"Вакансия: {self.name}"]
        if self.salary:
            text_parts.append(f"Зарплата: {self.salary}")
        text_parts.extend(
            (
                f"Опыт: {self.experience}",
                f"Занятость: {self.employment}",
                f"График работы: {self.schedule}",
            )
        )
        if self.work_formats:
            text_parts.append(f"Формат работы: {' '.join(self.work_formats)}")
        if self.key_skills:
            text_parts.append(f"Ключевые навыки: {' '.join(self.key_skills)}")
        text_parts.append(f"Описание: \n{self.description}")

        return "\n".join(text_parts)


class HeadHunterVacancyRead(BaseVacancyRead, BaseHeadHunterVacancy):
    pass


class BaseTelegramVacancy(BaseVacancy):
    channel_username: str
    message_id: int


class TelegramVacancyCreate(BaseVacancyCreate, BaseTelegramVacancy):
    data: str

    @property
    @computed_field
    def hash(self) -> str:
        return generate_hash(f"{self.link}:{self.message_id}")


class TelegramVacancyRead(BaseVacancyRead, BaseTelegramVacancy):
    pass
