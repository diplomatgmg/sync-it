from collections.abc import Sequence

from database.models import Vacancy
from database.models.enums import GradeEnum, ProfessionEnum, WorkFormatEnum
from repositories import VacancyRepository


__all__ = ["VacancyService"]


class VacancyService:
    """Сервис для бизнес-операций с вакансиями."""

    def __init__(self, repo: VacancyRepository) -> None:
        self.repo = repo

    async def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в сессию."""
        self.repo.add(vacancy)

    async def get_vacancies(
        self,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
    ) -> Sequence[Vacancy]:
        """Получает вакансии с применением фильтров."""
        return await self.repo.get_filtered(
            professions=professions,
            grades=grades,
            work_formats=work_formats,
        )
