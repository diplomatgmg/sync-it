from collections.abc import Iterable, Sequence

from common.shared.services import BaseUOWService
from database.models import Vacancy
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from schemas.grade import GradeRead
from schemas.skill import SkillRead
from schemas.vacancy import VacanciesSummarySchema, VacancyCreate, VacancyRead
from schemas.work_format import WorkFormatRead
from unitofwork import UnitOfWork


__all__ = ["VacancyService"]


class VacancyService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций с вакансиями."""

    async def add_vacancy(
        self,
        vacancy: VacancyCreate,
        grades: list[GradeRead],
        work_formats: list[WorkFormatRead],
        skills: list[SkillRead],
    ) -> VacancyRead:
        """Добавляет вакансию в сессию."""
        vacancy_model = Vacancy(**vacancy.model_dump())

        grade_models = await self._uow.grades.get_by_ids([g.id for g in grades])
        work_format_models = await self._uow.work_formats.get_by_ids([wf.id for wf in work_formats])
        skill_models = await self._uow.skills.get_by_ids([s.id for s in skills])

        vacancy_model.grades = list(grade_models)
        vacancy_model.work_formats = list(work_format_models)
        vacancy_model.skills = list(skill_models)

        created_vacancy = await self._uow.vacancies.add(vacancy_model)

        return VacancyRead.model_validate(created_vacancy)

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        return await self._uow.vacancies.get_existing_hashes(hashes)

    async def get_vacancies(self, limit: int) -> list[VacancyRead]:
        """Получает вакансии с применением фильтров."""
        vacancies = await self._uow.vacancies.get_all(limit=limit)

        return [VacancyRead.model_validate(v) for v in vacancies]

    async def get_vacancy_with_neighbors(
        self,
        vacancy_id: int | None,
        professions: Sequence[ProfessionEnum],
        grades: Sequence[GradeEnum],
        work_formats: Sequence[WorkFormatEnum],
        skills: Sequence[SkillEnum],
    ) -> tuple[int | None, VacancyRead | None, int | None]:
        if not skills:
            return None, None, None

        prev_id, vacancy, next_id = await self._uow.vacancies.get_relevant_with_neighbors(
            vacancy_id=vacancy_id,
            professions=professions,
            grades=grades,
            work_formats=work_formats,
            skills=skills,
        )

        if not vacancy:
            return None, None, None

        return prev_id, VacancyRead.model_validate(vacancy), next_id

    async def get_summary_vacancies(self) -> VacanciesSummarySchema:
        return await self._uow.vacancies.get_summary()
