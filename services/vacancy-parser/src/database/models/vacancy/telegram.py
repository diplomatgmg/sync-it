from database.models.enums import SourceEnum
from database.models.vacancy import BaseVacancy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["TelegramVacancy"]


class TelegramVacancy(BaseVacancy):
    __tablename__ = "telegram_vacancy"

    channel_username: Mapped[str] = mapped_column(String(32))
    message_id: Mapped[int] = mapped_column()

    def get_source(self) -> SourceEnum:  # noqa: PLR6301
        return SourceEnum.TELEGRAM
