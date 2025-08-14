from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime
from typing import TYPE_CHECKING

from common.shared.services import BaseUOWService
from schemas.vacancy import VacancyCreate, VacancyRead
from unitofwork import UnitOfWork


__all__ = ["AbstractVacancyService"]

if TYPE_CHECKING:
    from repositories import VacancyRepository


class AbstractVacancyService[
    VacancyReadType: VacancyRead,
    VacancyCreateType: VacancyCreate,
    VacancyRepositoryType: VacancyRepository,
](BaseUOWService[UnitOfWork], ABC):
    _read_schema: type[VacancyReadType]
    _create_schema: type[VacancyCreateType]
    _repo: "VacancyRepositoryType"

    def __init__(self, uow: "UnitOfWork") -> None:
        super().__init__(uow)
        self._repo = self._get_repo()

    @abstractmethod
    def _get_repo(self) -> "VacancyRepositoryType":
        pass

    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> VacancyReadType | None:
        duplicate = await self._repo.find_duplicate_vacancy_by_fingerprint(fingerprint)
        if not duplicate:
            return None

        return self._read_schema.model_validate(duplicate)

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        return await self._repo.get_similarity_score(fingerprint1, fingerprint2)

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        return await self._repo.get_existing_hashes(hashes)

    async def get_recent_vacancies(self, limit: int = 100) -> list[VacancyReadType]:
        """Получает последние актуальные вакансии из всех источников."""
        vacancies = await self._repo.get_recent_vacancies(limit=limit)
        return [self._read_schema.model_validate(v) for v in vacancies]

    async def update_vacancy_published_at(self, vacancy_hash: str, published_at: datetime) -> bool:
        """Обновляет дату публикации вакансии по её хэшу."""
        return await self._repo.update_published_at(vacancy_hash, published_at)

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """Помечает вакансию как удаленную по её хешу."""
        return await self._repo.mark_as_deleted(vacancy_hash=vacancy_hash)
