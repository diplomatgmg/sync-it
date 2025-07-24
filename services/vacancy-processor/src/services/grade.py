from collections.abc import Sequence

from database.models import Grade
from database.models.enums import GradeEnum
from repositories import GradeRepository


__all__ = ["GradeService"]


class GradeService:
    """Сервис для бизнес-операций, связанных с грейдами."""

    def __init__(self, repo: GradeRepository) -> None:
        self.repo = repo

    async def get_grade_by_name(self, name: GradeEnum) -> Grade | None:
        return await self.repo.get_by_name(name)

    async def get_grades(self) -> Sequence[Grade]:
        return await self.repo.get_all()

    async def add_grade(self, grade_enum: GradeEnum) -> None:
        """Создает экземпляр Grade и добавляет его в сессию через репозиторий."""
        grade_model = Grade(name=grade_enum)
        await self.repo.add(grade_model)
