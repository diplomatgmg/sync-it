from datetime import datetime

from database.models import Base
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Vacancy"]


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    hash: Mapped[str] = mapped_column(String(32), unique=True)
    fingerprint: Mapped[str] = mapped_column(Text, unique=True)
    link: Mapped[str] = mapped_column(String(256), unique=True)
    data: Mapped[str] = mapped_column(Text)

    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    __mapper_args__ = {  # noqa: RUF012
        "polymorphic_on": source,
        "polymorphic_identity": "base",
    }
