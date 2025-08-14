from datetime import datetime

from database.models.enums import SourceEnum
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

    @computed_field  # type: ignore[prop-decorator]
    @property
    def source(self) -> SourceEnum:
        raise NotImplementedError("Define source in child class")


class BaseVacancyCreate(BaseVacancy):
    pass


class BaseVacancyRead(BaseVacancy):
    id: int
    hash: str
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class VacancyRead(BaseVacancyRead, BaseVacancy):
    pass


class BaseHeadHunterVacancy(BaseVacancy):
    vacancy_id: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def source(self) -> SourceEnum:
        return SourceEnum.HEAD_HUNTER


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


class HeadHunterVacancyRead(BaseVacancyRead, BaseHeadHunterVacancy):
    pass


class BaseTelegramVacancy(BaseVacancy):
    channel_username: str
    message_id: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def source(self) -> SourceEnum:
        return SourceEnum.TELEGRAM


class TelegramVacancyCreate(BaseVacancyCreate, BaseTelegramVacancy):
    data: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def hash(self) -> str:
        return generate_hash(f"{self.link}:{self.message_id}")


class TelegramVacancyRead(BaseVacancyRead, BaseTelegramVacancy):
    pass
