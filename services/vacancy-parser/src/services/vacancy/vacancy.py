from collections.abc import Iterable
from datetime import datetime

from common.logger import get_logger
from database.models import Vacancy
from repositories import VacancyRepository
from schemas.vacancy import VacancyCreate, VacancyRead
from unitofwork import UnitOfWork

from services import BaseVacancyService


__all__ = ["VacancyService"]


logger = get_logger(__name__)


class VacancyService(BaseVacancyService):
    _read_schema: type[VacancyRead] = VacancyRead
    _create_schema: type[VacancyCreate] = VacancyCreate
    _repo: VacancyRepository[Vacancy]

    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)
        self._repo = self._get_repo()

    def _get_repo(self) -> VacancyRepository[Vacancy]:
        return self._uow.vacancies

    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> VacancyRead | None:
        duplicate = await self._repo.find_duplicate_vacancy_by_fingerprint(fingerprint)
        if not duplicate:
            return None

        return self._read_schema.model_validate(duplicate)

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        return await self._repo.get_similarity_score(fingerprint1, fingerprint2)

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        return await self._repo.get_existing_hashes(hashes)

    async def get_recent_vacancies(self, limit: int = 100) -> list[VacancyRead]:
        """Получает последние актуальные вакансии из всех источников."""
        vacancies = await self._repo.get_recent_vacancies(limit=limit)
        return [self._read_schema.model_validate(v) for v in vacancies]

    async def update_vacancy_published_at(self, vacancy_hash: str, published_at: datetime) -> bool:
        """Обновляет дату публикации вакансии по её хэшу."""
        return await self._repo.update_published_at(vacancy_hash, published_at)

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """Помечает вакансию как удаленную по её хешу."""
        return await self._repo.mark_as_deleted(vacancy_hash=vacancy_hash)
