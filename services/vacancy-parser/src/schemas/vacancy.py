from datetime import datetime

from common.shared.schemas import HttpsUrl
from database.models.enums import SourceEnum
from pydantic import BaseModel, ConfigDict, Field, computed_field
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
    link: HttpsUrl
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
    processed_at: datetime | None

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
    # Exclude поля нужны для расчета data. Для модели они лишние
    employer: str = Field(exclude=True)
    name: str = Field(exclude=True)
    description: str = Field(exclude=True)
    salary: str | None = Field(exclude=True)
    experience: str = Field(exclude=True)
    employment: str = Field(exclude=True)
    schedule: str = Field(exclude=True)
    work_formats: list[str] = Field(exclude=True)
    key_skills: list[str] = Field(exclude=True)

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
