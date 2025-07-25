from collections.abc import Sequence

from common.shared.repositories import BaseRepository
from database.models import Grade
from database.models.enums import GradeEnum
from sqlalchemy import select


__all__ = ["GradeRepository"]


class GradeRepository(BaseRepository):
    """Репозиторий для управления грейдами в базе данных."""

    async def get_by_name(self, name: GradeEnum) -> Grade | None:
        """Находит грейд по его имени (Enum)."""
        stmt = select(Grade).where(Grade.name == name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Grade]:
        """Возвращает все существующие грейды."""
        stmt = select(Grade)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def add(self, grade_model: Grade) -> None:
        """Добавляет новый экземпляр грейда в сессию."""
        self._session.add(grade_model)
