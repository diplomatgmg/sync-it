from database.models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Vacancy"]


class Vacancy(Base):
    __abstract__ = True

    hash: Mapped[str] = mapped_column(String(32), primary_key=True, unique=True)
    link: Mapped[str] = mapped_column(String(256), unique=True)
