from collections.abc import Sequence

from database.models.vacancy import BaseVacancy
from repositories.vacancy import VacancyRepository


__all__ = ["VacancyService"]


class VacancyService:
    """Сервис для бизнес-логики, связанной с вакансиями."""

    def __init__(self, vacancy_repo: VacancyRepository) -> None:
        self.repo = vacancy_repo

    async def get_recent_vacancies(self, limit: int = 100) -> Sequence[BaseVacancy]:
        """Получает последние актуальные вакансии из всех источников."""
        return await self.repo.get_recent_vacancies(limit=limit)

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """Помечает вакансию как удаленную по её хешу."""
        return await self.repo.mark_as_deleted(vacancy_hash=vacancy_hash)
