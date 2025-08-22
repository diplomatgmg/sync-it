from collections.abc import Iterable, Sequence

from common.shared.repositories import BaseRepository
from database.models import Skill
from database.models.enums import SkillEnum
from sqlalchemy import select


__all__ = ["SkillRepository"]


class SkillRepository(BaseRepository):
    """Репозиторий для управления навыками."""

    async def get_by_name(self, name: SkillEnum) -> Skill | None:
        stmt = select(Skill).where(Skill.name == name)
        result = await self._session.execute(stmt)

        return result.scalar_one()

    async def get_all(self) -> Sequence[Skill]:
        stmt = select(Skill)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_by_ids(self, ids: Iterable[int]) -> Sequence[Skill]:
        """Возвращает форматы работы по списку ID."""
        if not ids:
            return []

        stmt = select(Skill).where(Skill.id.in_(ids))
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_by_enums(self, enums: Iterable[SkillEnum]) -> Sequence[Skill]:
        stmt = select(Skill).where(Skill.name.in_(enums))
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def add(self, skill: Skill) -> Skill:
        self._session.add(skill)
        await self._session.flush()
        await self._session.refresh(skill)

        return skill
