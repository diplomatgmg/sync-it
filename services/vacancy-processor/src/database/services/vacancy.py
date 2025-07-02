from collections.abc import Sequence

from database.models import Grade, Profession, Vacancy, WorkFormat
from database.models.enums import GradeEnum, ProfessionEnum, WorkFormatEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


__all__ = ["VacancyService"]


class VacancyService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_vacancy(self, vacancy: Vacancy) -> Vacancy:
        self.session.add(vacancy)
        await self.session.commit()
        await self.session.refresh(vacancy)

        return vacancy

    async def get_vacancies(
        self,
        professions: Sequence[ProfessionEnum] | None = None,
        grades: Sequence[GradeEnum] | None = None,
        work_formats: Sequence[WorkFormatEnum] | None = None,
    ) -> Sequence[Vacancy]:
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

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()
