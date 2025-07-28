from collections.abc import Sequence

from common.shared.services import BaseService
from database.models import Vacancy
from database.models.enums import GradeEnum, ProfessionEnum, WorkFormatEnum
from repositories import VacancyRepository


__all__ = ["VacancyService"]


class VacancyService(BaseService[VacancyRepository]):
    """Сервис для бизнес-операций с вакансиями."""

    async def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в сессию."""
        self._repo.add(vacancy)

    async def get_vacancies(
        self,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
        limit: int | None = None,
    ) -> Sequence[Vacancy]:
        """Получает вакансии с применением фильтров."""
        return await self._repo.get_filtered(
            professions=professions,
            grades=grades,
            work_formats=work_formats,
            limit=limit,
        )
