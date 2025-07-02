from collections.abc import Sequence

from database.models import Grade
from database.models.enums import GradeEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["GradeService"]


class GradeService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_grade_by_name(self, name: GradeEnum) -> Grade:
        stmt = select(Grade).where(Grade.name == name)
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def get_grades(self) -> Sequence[Grade]:
        stmt = select(Grade)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def add_grade(self, grade: GradeEnum) -> Grade:
        grade_model = Grade(name=grade)

        self.session.add(grade_model)
        await self.session.commit()
        await self.session.refresh(grade_model)

        return grade_model
