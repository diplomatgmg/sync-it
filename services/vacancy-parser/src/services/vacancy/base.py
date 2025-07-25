from collections.abc import Iterable
from typing import Any, TypeVar

from common.shared.services import BaseService
from repositories.vacancy import VacancyRepository


__all__ = ["BaseVacancyService"]


RepoType = TypeVar("RepoType", bound=VacancyRepository)


class BaseVacancyService(BaseService[RepoType]):
    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> Any | None:
        return await self._repo.find_duplicate_vacancy_by_fingerprint(fingerprint)

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        return await self._repo.get_similarity_score(fingerprint1, fingerprint2)

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        return await self._repo.get_existing_hashes(hashes)
