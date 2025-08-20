from collections.abc import Sequence

from common.shared.repositories import BaseRepository
from database.models import Profession
from database.models.enums import ProfessionEnum
from sqlalchemy import select


__all__ = ["ProfessionRepository"]


class ProfessionRepository(BaseRepository):
    """Репозиторий для управления профессиями в базе данных."""

    async def get_by_name(self, name: ProfessionEnum) -> Profession:
        """Находит профессию по имени."""
        stmt = select(Profession).where(Profession.name == name)
        result = await self._session.execute(stmt)

        return result.scalar_one()

    async def get_all(self) -> Sequence[Profession]:
        """Возвращает все профессии."""
        stmt = select(Profession)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def add(self, profession: Profession) -> Profession:
        """Добавляет экземпляр профессии в сессию."""
        self._session.add(profession)
        await self._session.flush()
        await self._session.refresh(profession)

        return profession
