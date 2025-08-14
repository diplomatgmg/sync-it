from common.shared.services import BaseUOWService
from database.models import Grade
from database.models.enums import GradeEnum
from schemas.grade import GradeCreate, GradeRead
from unitofwork import UnitOfWork


__all__ = ["GradeService"]


class GradeService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций, связанных с грейдами."""

    async def get_grade_by_name(self, name: GradeEnum) -> GradeRead | None:
        grade = await self._uow.grades.get_by_name(name)

        return GradeRead.model_validate(grade)

    async def get_grades(self) -> list[GradeRead]:
        grades = await self._uow.grades.get_all()

        return [GradeRead.model_validate(g) for g in grades]

    async def add_grade(self, grade: GradeCreate) -> GradeRead:
        grade_model = Grade(**grade.model_dump())
        created_grade = await self._uow.grades.add(grade_model)

        return GradeRead.model_validate(created_grade)
