from collections.abc import Sequence

from common.shared.services import BaseService
from database.models import Vacancy
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
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
        skills: Sequence[SkillEnum] | None = None,
        limit: int | None = None,
    ) -> Sequence[Vacancy]:
        """Получает вакансии с применением фильтров."""
        return await self._repo.get_filtered(
            professions=professions,
            grades=grades,
            work_formats=work_formats,
            skills=skills,
            limit=limit,
        )

    async def get_vacancy_with_neighbors(
        self,
        vacancy_id: int,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
        skills: Sequence[SkillEnum] | None = None,
    ) -> tuple[int | None, Vacancy | None, int | None]:
        vacancy = await self._repo.get_by_id(vacancy_id)
        if not vacancy:
            return None, None, None

        professions = professions or []
        grades = grades or []
        work_formats = work_formats or []
        skills = skills or []

        prev_id = await self._repo.get_prev_id(
            vacancy.published_at, vacancy.id, professions, grades, work_formats, skills
        )
        next_id = await self._repo.get_next_id(
            vacancy.published_at, vacancy.id, professions, grades, work_formats, skills
        )

        return prev_id, vacancy, next_id
