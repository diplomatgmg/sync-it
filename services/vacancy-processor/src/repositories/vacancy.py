from collections.abc import Sequence

from common.shared.repositories import BaseRepository
from database.models import Grade, Profession, Vacancy, WorkFormat
from database.models.enums import GradeEnum, ProfessionEnum, WorkFormatEnum
from sqlalchemy import select
from sqlalchemy.orm import joinedload


__all__ = ["VacancyRepository"]


class VacancyRepository(BaseRepository):
    """Репозиторий для управления вакансиями."""

    def add(self, vacancy: Vacancy) -> None:
        """Добавляет экземпляр вакансии в сессию."""
        self._session.add(vacancy)

    async def get_filtered(
        self,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
    ) -> Sequence[Vacancy]:
        """Получает отфильтрованный список вакансий."""
        professions = professions or []
        grades = grades or []
        work_formats = work_formats or []

        stmt = (
            select(Vacancy)
            .options(
                joinedload(Vacancy.profession),
                joinedload(Vacancy.grades),
                joinedload(Vacancy.work_formats),
            )
            .order_by(Vacancy.id)
        )

        if professions:
            stmt = stmt.filter(Vacancy.profession.has(Profession.name.in_(professions)))
        if grades:
            stmt = stmt.filter(Vacancy.grades.any(Grade.name.in_(grades)))
        if work_formats:
            stmt = stmt.filter(Vacancy.work_formats.any(WorkFormat.name.in_(work_formats)))

        result = await self._session.execute(stmt)
        return result.scalars().unique().all()
