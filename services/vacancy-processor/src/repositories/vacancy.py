from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

from common.shared.repositories import BaseRepository
from database.models import Grade, Profession, Skill, Vacancy, WorkFormat
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from sqlalchemy import Select, func, select
from sqlalchemy.orm import joinedload


__all__ = ["VacancyRepository"]

TSelect = TypeVar("TSelect", bound=Select[Any])


class VacancyRepository(BaseRepository):
    """Репозиторий для управления вакансиями."""

    async def add(self, vacancy: Vacancy) -> Vacancy:
        """Добавляет экземпляр вакансии в сессию."""
        self._session.add(vacancy)
        await self._session.flush()
        await self._session.refresh(vacancy, attribute_names=["profession", "skills", "grades", "work_formats"])

        return vacancy

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        """Получить set уже существующих хешей в БД."""
        stmt = select(Vacancy.hash).where(Vacancy.hash.in_(hashes))
        result = await self._session.execute(stmt)

        return set(result.scalars().all())

    async def get_by_id(self, vacancy_id: int) -> Vacancy | None:
        """Получает вакансию по ее id."""
        stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)
        result = await self._session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def get_all(self, limit: int) -> Sequence[Vacancy]:
        """Получает отфильтрованный список вакансий."""
        stmt = select(Vacancy)
        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)
        stmt = stmt.order_by(Vacancy.published_at.desc()).limit(limit)

        result = await self._session.execute(stmt)

        return result.scalars().unique().all()

    async def get_with_neighbors(
        self,
        vacancy_id: int | None,
        professions: Sequence[ProfessionEnum],
        grades: Sequence[GradeEnum],
        work_formats: Sequence[WorkFormatEnum],
        skills: Sequence[SkillEnum],
    ) -> tuple[int | None, Vacancy | None, int | None]:
        # Базовый запрос с фильтрацией
        filtered_ids_stmt = select(Vacancy.id)
        if professions:
            filtered_ids_stmt = filtered_ids_stmt.filter(Vacancy.profession.has(Profession.name.in_(professions)))
        if grades:
            filtered_ids_stmt = filtered_ids_stmt.filter(Vacancy.grades.any(Grade.name.in_(grades)))
        if work_formats:
            filtered_ids_stmt = filtered_ids_stmt.filter(Vacancy.work_formats.any(WorkFormat.name.in_(work_formats)))

        # Создаем CTE с оконными функциями
        ranked_vacancies_cte = (
            select(
                Vacancy.id.label("vacancy_id"),
                func.lag(Vacancy.id).over(order_by=Vacancy.published_at.desc()).label("prev_id"),
                func.lead(Vacancy.id).over(order_by=Vacancy.published_at.desc()).label("next_id"),
            )
            .where(Vacancy.id.in_(filtered_ids_stmt))
            .cte("ranked_vacancies")
        )

        # Основной запрос
        stmt = select(
            ranked_vacancies_cte.c.prev_id,
            Vacancy,
            ranked_vacancies_cte.c.next_id,
        ).join(ranked_vacancies_cte, Vacancy.id == ranked_vacancies_cte.c.vacancy_id)

        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)

        if vacancy_id:
            stmt = stmt.where(Vacancy.id == vacancy_id)
        else:
            stmt = stmt.order_by(Vacancy.published_at.desc()).limit(1)

        result = await self._session.execute(stmt)
        row = result.first()

        if not row:
            return None, None, None

        return row.prev_id, row.Vacancy, row.next_id

    @staticmethod
    def _apply_vacancy_prefetch_details_to_stmt(stmt: TSelect) -> TSelect:
        return stmt.options(
            joinedload(Vacancy.profession),
            joinedload(Vacancy.grades),
            joinedload(Vacancy.work_formats),
            joinedload(Vacancy.skills),
        )
