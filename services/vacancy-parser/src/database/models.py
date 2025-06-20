from abc import abstractmethod
from datetime import datetime
from typing import Any, Self

from schemas import TelegramChannelUrl
from sqlalchemy import DateTime, MetaData, String, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from utils import generate_hash


metadata_obj = MetaData(schema="vacancy_parser")


# len("https://t.me/s/") + len("channel_name")  # noqa: ERA001
MAX_CHANNEL_LINK_LENGTH = 143


class Base(DeclarativeBase, AsyncAttrs):
    metadata = metadata_obj


class BaseVacancy(Base):
    __abstract__ = True

    hash: Mapped[str] = mapped_column(String(32), primary_key=True, unique=True)

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> Self:
        """Создает экземпляр вакансии автоматически генерируя хеша"""


class Vacancy(BaseVacancy):
    __tablename__ = "vacancy"

    name: Mapped[str] = mapped_column(String(256))
    link: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime())


class TelegramVacancy(BaseVacancy):
    __tablename__ = "telegram_vacancy"

    channel_link: Mapped[TelegramChannelUrl] = mapped_column(String(MAX_CHANNEL_LINK_LENGTH))
    message_id: Mapped[int]
    message: Mapped[str] = mapped_column(String(4096))

    __table_args__ = (
        UniqueConstraint("channel_link", "message_id", name="uq_telegram_vacancy_channel_message"),
    )

    @classmethod
    def create(cls, channel_link: TelegramChannelUrl, message_id: int, message: str) -> "TelegramVacancy":
        hash_value = generate_hash(f"{channel_link}:{message_id}")
        return cls(
            hash=hash_value,
            channel_link=str(channel_link),
            message_id=message_id,
            message=message,
        )
