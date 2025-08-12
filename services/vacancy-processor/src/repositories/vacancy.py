from collections.abc import Sequence
from datetime import datetime
from typing import Any, TypeVar

from common.shared.repositories import BaseRepository
from database.models import Grade, Profession, Skill, Vacancy, WorkFormat
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload


__all__ = ["VacancyRepository"]

TSelect = TypeVar("TSelect", bound=Select[Any])


class VacancyRepository(BaseRepository):
    """Репозиторий для управления вакансиями."""

    async def add(self, vacancy: Vacancy) -> Vacancy:
        """Добавляет экземпляр вакансии в сессию."""
        self._session.add(vacancy)
        await self._session.flush()
        await self._session.refresh(vacancy)

        return vacancy

    async def get_by_id(self, vacancy_id: int) -> Vacancy | None:
        """Получает вакансию по ее id."""
        stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)
        result = await self._session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def get_filtered(
        self,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
        skills: Sequence[SkillEnum] | None = None,
        limit: int | None = None,
    ) -> Sequence[Vacancy]:
        """Получает отфильтрованный список вакансий."""
        professions = professions or []
        grades = grades or []
        work_formats = work_formats or []
        skills = skills or []
        limit = limit or 10

        stmt = select(Vacancy)
        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)
        stmt = self._apply_filters_to_stmt(stmt, professions, grades, work_formats, skills)
        stmt = stmt.order_by(Vacancy.published_at.desc()).limit(limit)

        result = await self._session.execute(stmt)

        return result.scalars().unique().all()

    async def get_prev_id(
        self,
        published_at: datetime,
        vacancy_id: int,
        professions: Sequence[ProfessionEnum],
        grades: Sequence[GradeEnum],
        work_formats: Sequence[WorkFormatEnum],
        skills: Sequence[SkillEnum],
    ) -> int | None:
        stmt = select(Vacancy.id).where(
            (Vacancy.published_at > published_at) | ((Vacancy.published_at == published_at) & (Vacancy.id > vacancy_id))
        )

        stmt = self._apply_filters_to_stmt(stmt, professions, grades, work_formats, skills)

        stmt = stmt.order_by(Vacancy.published_at.asc(), Vacancy.id.asc()).limit(1)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_next_id(
        self,
        published_at: datetime,
        vacancy_id: int,
        professions: Sequence[ProfessionEnum],
        grades: Sequence[GradeEnum],
        work_formats: Sequence[WorkFormatEnum],
        skills: Sequence[SkillEnum],
    ) -> int | None:
        stmt = select(Vacancy.id).where(
            (Vacancy.published_at < published_at) | ((Vacancy.published_at == published_at) & (Vacancy.id < vacancy_id))
        )

        # И здесь тоже применяем фильтры!
        stmt = self._apply_filters_to_stmt(stmt, professions, grades, work_formats, skills)

        stmt = stmt.order_by(Vacancy.published_at.desc(), Vacancy.id.desc()).limit(1)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def _apply_vacancy_prefetch_details_to_stmt(stmt: TSelect) -> TSelect:
        return stmt.options(
            joinedload(Vacancy.profession),
            joinedload(Vacancy.grades),
            joinedload(Vacancy.work_formats),
        )

    @staticmethod
    def _apply_filters_to_stmt(
        stmt: TSelect,
        professions: Sequence[ProfessionEnum],
        grades: Sequence[GradeEnum],
        work_formats: Sequence[WorkFormatEnum],
        skills: Sequence[SkillEnum],
    ) -> TSelect:
        if professions:
            stmt = stmt.filter(Vacancy.profession.has(Profession.name.in_(professions)))
        if grades:
            stmt = stmt.filter(Vacancy.grades.any(Grade.name.in_(grades)))
        if work_formats:
            stmt = stmt.filter(Vacancy.work_formats.any(WorkFormat.name.in_(work_formats)))
        if skills:
            stmt = stmt.filter(Vacancy.skills.any(Skill.name.in_(skills)))
        return stmt
