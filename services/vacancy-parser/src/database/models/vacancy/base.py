from datetime import datetime
from typing import Any, Self

from database.models import Base
from database.models.enums import SourceEnum
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["BaseVacancy"]


class BaseVacancy(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(32), unique=True)
    fingerprint: Mapped[str] = mapped_column(Text, unique=True)

    source_id: Mapped[int] = mapped_column(ForeignKey("source.id", ondelete="RESTRICT"), index=True)

    link: Mapped[str] = mapped_column(String(256), unique=True)
    data: Mapped[str] = mapped_column(String(8192))

    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
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

    def get_source(self) -> SourceEnum:
        raise NotImplementedError(f"Implement {self.__class__.__name__}.get_source()")
