from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):
    __table_args__ = {"schema": "parser"}  # noqa: RUF012


class RawVacancy(Base):
    __tablename__ = "raw_vacancy"
