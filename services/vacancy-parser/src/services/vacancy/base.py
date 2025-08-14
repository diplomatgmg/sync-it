from collections.abc import Iterable

from common.shared.services.base import BaseUOWService
from schemas.vacancy import BaseVacancyCreate, BaseVacancyRead
from unitofwork import UnitOfWork


__all__ = [
    "BaseVacancyService",
]


class BaseVacancyService(BaseUOWService[UnitOfWork]):
    vacancy_create_schema: BaseVacancyCreate
    vacancy_read_schema: BaseVacancyRead

    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> BaseVacancyRead | None:
        duplicate = await self._uow.vacancies.find_duplicate_vacancy_by_fingerprint(fingerprint)

        return self.vacancy_read_schema.model_validate(duplicate) if duplicate else None

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        return await self._uow.vacancies.get_similarity_score(fingerprint1, fingerprint2)

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        return await self._uow.vacancies.get_existing_hashes(hashes)
