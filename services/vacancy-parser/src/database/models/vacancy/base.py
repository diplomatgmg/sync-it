from datetime import UTC, datetime
from typing import Any, Self

from database.models import Base
from database.models.vacancy.enums import VacancySource
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["BaseVacancy"]


def _utcnow() -> datetime:
    return datetime.now(tz=UTC)


class BaseVacancy(Base):
    __abstract__ = True

    hash: Mapped[str] = mapped_column(String(32), primary_key=True)
    fingerprint: Mapped[str] = mapped_column(Text)
    source: Mapped[VacancySource] = mapped_column(SQLEnum(VacancySource, schema="vacancy_parser"), index=True)
    link: Mapped[str] = mapped_column(String(256), unique=True)
    data: Mapped[str] = mapped_column(String(8192))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if not kwargs.get("hash"):
            raise ValueError(f"Use {self.__class__.__name__}.create() instead {self.__class__.__name__}()")

        self.source = self.get_source()

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> Self:
        """Создает экземпляр вакансии генерируя хеш"""
        raise NotImplementedError(f"Implement {cls.__name__}.create()")

    def get_source(self) -> VacancySource:
        raise NotImplementedError(f"Implement {self.__class__.__name__}.get_source()")
