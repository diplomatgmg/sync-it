from collections.abc import Iterable
from typing import Any

from repositories.vacancy import TelegramVacancyRepository, VacancyRepository


__all__ = ["BaseVacancyService"]


class BaseVacancyService:
    repo: VacancyRepository | TelegramVacancyRepository

    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> Any | None:
        return await self.repo.find_duplicate_vacancy_by_fingerprint(fingerprint)

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        return await self.repo.get_similarity_score(fingerprint1, fingerprint2)

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        return await self.repo.get_existing_hashes(hashes)
