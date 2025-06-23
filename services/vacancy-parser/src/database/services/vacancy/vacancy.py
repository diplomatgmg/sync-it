from collections.abc import Iterable

from database.models.vacancy import BaseVacancy
from database.models.vacancy.enums import VacancySource
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils import required_attrs


__all__ = ["VacancyService"]


class VacancyService:
    """Базовый сервис для работы с моделями вакансий."""

    source: VacancySource
    model: type[BaseVacancy]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_vacancies(self, limit: int = 100) -> list[BaseVacancy]:
        """Получить последние актуальные вакансии по всем сервисам."""
        vacancies: list[BaseVacancy] = []

        subclasses = BaseVacancy.__subclasses__()

        for subclass in subclasses:
            stmt = select(subclass).order_by(subclass.created_at.desc()).limit(limit)
            result = await self.session.execute(stmt)
            vacancies.extend(result.scalars().all())

        vacancies.sort(key=lambda x: x.created_at, reverse=True)
        return vacancies[:limit]

    async def bulk_add_vacancies(self, vacancies: list[type[BaseVacancy]]) -> int:
        """Массовое добавление вакансий."""
        added_count = 0

        for vacancy in vacancies:
            self.session.add(vacancy)
            added_count += 1

        await self.session.commit()
        return added_count

    @required_attrs("model")
    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        """Получить set уже существующих хешей в БД."""
        stmt = select(self.model.hash).where(self.model.hash.in_(hashes))
        result = await self.session.execute(stmt)
        return {row[0] for row in result.fetchall()}
