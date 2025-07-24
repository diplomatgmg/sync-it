from collections.abc import Sequence

from database.models import WorkFormat
from database.models.enums import WorkFormatEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["WorkFormatRepository"]


class WorkFormatRepository:
    """Репозиторий для управления форматами работы."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, name: WorkFormatEnum) -> WorkFormat | None:
        """Находит формат работы по имени."""
        stmt = select(WorkFormat).where(WorkFormat.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[WorkFormat]:
        """Возвращает все форматы работы."""
        stmt = select(WorkFormat)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def add(self, work_format_model: WorkFormat) -> None:
        """Добавляет экземпляр формата работы в сессию."""
        self.session.add(work_format_model)
