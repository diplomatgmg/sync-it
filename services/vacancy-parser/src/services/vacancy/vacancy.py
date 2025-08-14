from schemas.vacancy import VacancyRead
from services.vacancy import BaseVacancyService


__all__ = ["VacancyService"]


class VacancyService(BaseVacancyService):
    """Сервис для бизнес-логики, связанной с вакансиями из разных источников."""

    async def get_recent_vacancies(self, limit: int = 100) -> list[VacancyRead]:
        """Получает последние актуальные вакансии из всех источников."""
        vacancies = await self._uow.vacancies.get_recent_vacancies(limit=limit)

        return [VacancyRead.model_validate(v) for v in vacancies]

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """Помечает вакансию как удаленную по её хешу."""
        return await self._uow.vacancies.mark_as_deleted(vacancy_hash=vacancy_hash)
