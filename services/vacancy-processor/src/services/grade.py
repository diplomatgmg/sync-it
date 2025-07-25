from collections.abc import Sequence

from common.shared.services import BaseService
from database.models import Grade
from database.models.enums import GradeEnum
from repositories import GradeRepository


__all__ = ["GradeService"]


class GradeService(BaseService[GradeRepository]):
    """Сервис для бизнес-операций, связанных с грейдами."""

    async def get_grade_by_name(self, name: GradeEnum) -> Grade | None:
        return await self._repo.get_by_name(name)

    async def get_grades(self) -> Sequence[Grade]:
        return await self._repo.get_all()

    async def add_grade(self, grade_enum: GradeEnum) -> None:
        """Создает экземпляр Grade и добавляет его в сессию через репозиторий."""
        grade_model = Grade(name=grade_enum)
        await self._repo.add(grade_model)
