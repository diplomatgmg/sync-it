from typing import Self

from database.models.enums import SourceEnum
from database.models.vacancy import BaseVacancy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from utils import generate_hash


__all__ = ["TelegramVacancy"]


class TelegramVacancy(BaseVacancy):
    __tablename__ = "telegram_vacancy"

    channel_username: Mapped[str] = mapped_column(String(32))
    message_id: Mapped[int] = mapped_column()

    @classmethod
    def create(
        cls, *, source_id: int, fingerprint: str, link: str, channel_username: str, message_id: int, data: str
    ) -> Self:
        """Создает экземпляр вакансии автоматически генерируя хеш"""
        hash_value = generate_hash(f"{link}:{message_id}")

        return cls(
            hash=hash_value,
            fingerprint=fingerprint,
            source_id=source_id,
            link=link,
            channel_username=channel_username,
            message_id=message_id,
            data=data,
        )

    def get_source(self) -> SourceEnum:  # noqa: PLR6301
        return SourceEnum.TELEGRAM
