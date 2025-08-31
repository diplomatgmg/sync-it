from collections.abc import Iterable

from common.redis.decorators.cache import build_key, cache
from common.shared.serializers.pickle import PickleSerializer
from common.shared.services import BaseUOWService
from database.models import Vacancy
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from schemas.grade import GradeRead
from schemas.skill import SkillRead
from schemas.vacancy import VacanciesSummarySchema, VacancyCreate, VacancyRead
from schemas.work_format import WorkFormatRead
from unitofwork import UnitOfWork


__all__ = ["VacancyService"]


def _neighbors_key_builder(
    _self: "VacancyService",
    professions: list[ProfessionEnum],
    grades: list[GradeEnum],
    work_formats: list[WorkFormatEnum],
    skills: list[SkillEnum],
) -> str:
    enums_str = sorted(map(str, [*professions, *grades, *work_formats, *skills]))

    return build_key(*enums_str)


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
        professions: list[ProfessionEnum],
        grades: list[GradeEnum],
        work_formats: list[WorkFormatEnum],
        skills: list[SkillEnum],
    ) -> tuple[int | None, VacancyRead | None, int | None]:
        if not skills:
            return None, None, None

        vacancies = await self._get_relevant_vacancies(
            professions=professions,
            grades=grades,
            work_formats=work_formats,
            skills=skills,
        )

        if not vacancies:
            return None, None, None

        if vacancy_id:
            try:
                index = next(i for i, v in enumerate(vacancies) if v.id == vacancy_id)
            except StopIteration:
                return None, None, None
        else:
            index = 0

        prev_id = vacancies[index - 1].id if index > 0 else None
        next_id = vacancies[index + 1].id if index < len(vacancies) - 1 else None
        current = vacancies[index]

        return prev_id, VacancyRead.model_validate(current), next_id

    async def get_summary_vacancies(self) -> VacanciesSummarySchema:
        return await self._uow.vacancies.get_summary()

    @cache(cache_ttl=60 * 10, key_builder=_neighbors_key_builder, serializer=PickleSerializer())
    async def _get_relevant_vacancies(
        self,
        professions: list[ProfessionEnum],
        grades: list[GradeEnum],
        work_formats: list[WorkFormatEnum],
        skills: list[SkillEnum],
    ) -> list[Vacancy]:
        """Возвращает только релевантные вакансии (для кеша)."""
        return await self._uow.vacancies.get_relevant(
            professions=professions,
            grades=grades,
            work_formats=work_formats,
            skills=skills,
        )
