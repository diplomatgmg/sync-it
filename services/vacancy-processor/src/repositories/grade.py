from collections.abc import Sequence

from common.shared.repositories import BaseRepository
from database.models import Grade
from database.models.enums import GradeEnum
from sqlalchemy import select


__all__ = ["GradeRepository"]


class GradeRepository(BaseRepository):
    """Репозиторий для управления грейдами в базе данных."""

    async def get_by_name(self, name: GradeEnum) -> Grade:
        """Находит грейд по его имени."""
        stmt = select(Grade).where(Grade.name == name)
        result = await self._session.execute(stmt)

        return result.scalar_one()

    async def get_all(self) -> Sequence[Grade]:
        """Возвращает все существующие грейды."""
        stmt = select(Grade)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_by_ids(self, ids: Sequence[int]) -> Sequence[Grade]:
        """Возвращает грейды по списку ID."""
        if not ids:
            return []

        stmt = select(Grade).where(Grade.id.in_(ids))
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def add(self, grade: Grade) -> Grade:
        """Добавляет новый экземпляр грейда в сессию."""
        self._session.add(grade)
        await self._session.flush()
        await self._session.refresh(grade)

        return grade
