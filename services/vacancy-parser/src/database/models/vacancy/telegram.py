from database.models.vacancy import BaseVacancy
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["TelegramVacancy"]


class TelegramVacancy(BaseVacancy):
    """Класс абстракции для работы с вакансиями из Telegram."""

    __tablename__ = "telegram_vacancy"

    message_id: Mapped[int] = mapped_column()
