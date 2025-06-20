from collections.abc import Iterable

from database.models.vacancy import TelegramVacancy
from database.models.vacancy.enums import VacancySource
from schemas import TelegramChannelUrl
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["TelegramVacancyService"]


class TelegramVacancyService:
    source = VacancySource.TELEGRAM

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def bulk_add_vacancies(self, vacancies: list[TelegramVacancy]) -> int:
        """Массовое добавление вакансий."""
        added_count = 0

        for vacancy in vacancies:
            self.session.add(vacancy)
            added_count += 1

        await self.session.commit()
        return added_count

    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        """Получить последний message_id для заданного Telegram канала."""
        smtp = select(func.max(TelegramVacancy.message_id)).where(
            (TelegramVacancy.source == self.source) & (TelegramVacancy.channel_username == link.channel_username)
        )
        result = await self.session.execute(smtp)
        return result.scalar_one_or_none()

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        """Получить set уже существующих хешей в БД."""
        stmt = select(TelegramVacancy.hash).where(TelegramVacancy.hash.in_(hashes))
        result = await self.session.execute(stmt)
        return {row[0] for row in result.fetchall()}
