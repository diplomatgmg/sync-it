from collections.abc import Sequence

from common.shared.repositories import BaseRepository
from database.models import WorkFormat
from database.models.enums import WorkFormatEnum
from sqlalchemy import select


__all__ = ["WorkFormatRepository"]


class WorkFormatRepository(BaseRepository):
    """Репозиторий для управления форматами работы."""

    async def get_by_name(self, name: WorkFormatEnum) -> WorkFormat | None:
        """Находит формат работы по имени."""
        stmt = select(WorkFormat).where(WorkFormat.name == name)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[WorkFormat]:
        """Возвращает все форматы работы."""
        stmt = select(WorkFormat)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def add(self, work_format: WorkFormat) -> WorkFormat:
        """Добавляет экземпляр формата работы в сессию."""
        self._session.add(work_format)
        await self._session.flush()
        await self._session.refresh(work_format)

        return work_format
