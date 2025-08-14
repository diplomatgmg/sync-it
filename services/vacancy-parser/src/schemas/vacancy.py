from datetime import datetime

from database.models.enums import SourceEnum
from pydantic import BaseModel, ConfigDict, computed_field
from utils import generate_hash


__all__ = [
    "HeadHunterVacancyCreate",
    "HeadHunterVacancyRead",
    "TelegramVacancyCreate",
    "TelegramVacancyRead",
    "VacancyCreate",
    "VacancyRead",
]


class BaseVacancy(BaseModel):
    source: SourceEnum
    fingerprint: str
    link: str
    published_at: datetime


class VacancyCreate(BaseVacancy):
    @computed_field  # type: ignore[prop-decorator]
    @property
    def hash(self) -> str:
        raise NotImplementedError("Define hash in child class")


class VacancyRead(BaseVacancy):
    id: int
    hash: str
    data: str
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class BaseTelegramVacancy(BaseVacancy):
    source: SourceEnum = SourceEnum.TELEGRAM
    channel_username: str
    message_id: int


class TelegramVacancyCreate(BaseTelegramVacancy, VacancyCreate):
    data: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def hash(self) -> str:
        return generate_hash(f"{self.link}:{self.message_id}")


class TelegramVacancyRead(BaseTelegramVacancy, VacancyRead):
    pass


class BaseHeadHunterVacancy(BaseVacancy):
    source: SourceEnum = SourceEnum.HEAD_HUNTER
    vacancy_id: int


class HeadHunterVacancyCreate(BaseHeadHunterVacancy, VacancyCreate):
    employer: str
    name: str
    description: str
    salary: str | None
    experience: str
    employment: str
    schedule: str
    work_formats: list[str]
    key_skills: list[str]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def hash(self) -> str:
        return generate_hash(self.vacancy_id)

    @computed_field  # type: ignore[prop-decorator]
    @property
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


class HeadHunterVacancyRead(BaseHeadHunterVacancy, VacancyRead):
    data: str
