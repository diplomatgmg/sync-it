from typing import Any, Self

from database.models import Base
from pydantic import HttpUrl
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from utils import generate_hash


__all__ = ["BaseVacancy"]


class BaseVacancy(Base):
    __abstract__ = True

    hash: Mapped[str] = mapped_column(String(32), primary_key=True, unique=True)
    link: Mapped[HttpUrl] = mapped_column(String(256), unique=True)
    data: Mapped[str] = mapped_column(String(8192))
    created_at: Mapped[DateTime] = mapped_column(DateTime())

    def __init__(self, **kwargs: Any) -> None:
        if not kwargs.get("hash"):  # FIXME Проверить работу
            raise ValueError(f"Use {self.__class__.__name__}.create() instead {self.__class__.__name__}()")
        super().__init__(**kwargs)

    @classmethod
    def create(cls, link: HttpUrl, **kwargs: Any) -> Self:
        """Создает экземпляр вакансии автоматически генерируя хеш"""
        vacancy_hash = generate_hash(str(link))
        return cls(hash=vacancy_hash, link=link, **kwargs)
