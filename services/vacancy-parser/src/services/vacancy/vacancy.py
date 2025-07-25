from collections.abc import Sequence

from database.models.vacancy import BaseVacancy
from repositories.vacancy import VacancyRepository
from services.vacancy import BaseVacancyService


__all__ = ["VacancyService"]


class VacancyService(BaseVacancyService[VacancyRepository]):
    """Сервис для бизнес-логики, связанной с вакансиями из разных источников."""

    async def get_recent_vacancies(self, limit: int = 100) -> Sequence[BaseVacancy]:
        """Получает последние актуальные вакансии из всех источников."""
        return await self._repo.get_recent_vacancies(limit=limit)

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """Помечает вакансию как удаленную по её хешу."""
        return await self._repo.mark_as_deleted(vacancy_hash=vacancy_hash)
