from collections.abc import Sequence

from common.shared.services.base import BaseUOWService
from database.models import Vacancy
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from schemas.vacancy import VacancyCreate, VacancyRead
from unitofwork import UnitOfWork


__all__ = ["VacancyService"]


class VacancyService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций с вакансиями."""

    async def add_vacancy(self, vacancy: VacancyCreate) -> VacancyRead:
        """Добавляет вакансию в сессию."""
        vacancy_model = Vacancy(**vacancy.model_dump())
        created_vacancy = await self._uow.vacancies.add(vacancy_model)

        return VacancyRead.model_validate(created_vacancy)

    async def get_vacancies(
        self,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
        skills: Sequence[SkillEnum] | None = None,
        limit: int | None = None,
    ) -> list[VacancyRead]:
        """Получает вакансии с применением фильтров."""
        vacancies = await self._uow.vacancies.get_filtered(
            professions=professions,
            grades=grades,
            work_formats=work_formats,
            skills=skills,
            limit=limit,
        )

        return [VacancyRead.model_validate(v) for v in vacancies]

    async def get_vacancy_with_neighbors(
        self,
        vacancy_id: int,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
        skills: Sequence[SkillEnum] | None = None,
    ) -> tuple[int | None, VacancyRead | None, int | None]:
        if vacancy_id == -1:
            vacancies = await self._uow.vacancies.get_filtered(professions, grades, work_formats, skills, limit=1)
            vacancy = vacancies[0] if vacancies else None
        else:
            vacancy = await self._uow.vacancies.get_by_id(vacancy_id)

        if not vacancy:
            return None, None, None

        professions = professions or []
        grades = grades or []
        work_formats = work_formats or []
        skills = skills or []

        prev_id = await self._uow.vacancies.get_prev_id(
            vacancy.published_at, vacancy.id, professions, grades, work_formats, skills
        )
        next_id = await self._uow.vacancies.get_next_id(
            vacancy.published_at, vacancy.id, professions, grades, work_formats, skills
        )

        return prev_id, VacancyRead.model_validate(vacancy), next_id
