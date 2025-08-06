from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

from common.shared.services import BaseService
from database.models.vacancy import BaseVacancy
from repositories.vacancy import VacancyRepository


__all__ = [
    "BaseVacancyService",
    "RepoType",
]


RepoType = TypeVar("RepoType", bound=VacancyRepository)


class BaseVacancyService(BaseService[RepoType]):
    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> Any | None:
        return await self._repo.find_duplicate_vacancy_by_fingerprint(fingerprint)

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        return await self._repo.get_similarity_score(fingerprint1, fingerprint2)

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        return await self._repo.get_existing_hashes(hashes)

    async def bulk_create(self, vacancies: Sequence[BaseVacancy]) -> int:
        return await self._repo.bulk_create(vacancies)
