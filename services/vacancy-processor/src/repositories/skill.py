from collections.abc import Sequence

from common.shared.repositories import BaseRepository
from database.models import Skill, SkillCategory
from database.models.enums import SkillCategoryEnum, SkillEnum
from sqlalchemy import select


__all__ = ["SkillCategoryRepository", "SkillRepository"]


class SkillCategoryRepository(BaseRepository):
    """Репозиторий для управления категориями навыков."""

    async def get_by_name(self, name: SkillCategoryEnum) -> SkillCategory | None:
        stmt = select(SkillCategory).where(SkillCategory.name == name)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[SkillCategory]:
        stmt = select(SkillCategory)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def add(self, category: SkillCategory) -> SkillCategory:
        self._session.add(category)
        await self._session.flush()
        await self._session.refresh(category)

        return category


class SkillRepository(BaseRepository):
    """Репозиторий для управления навыками."""

    async def get_by_name(self, name: SkillEnum) -> Skill | None:
        stmt = select(Skill).where(Skill.name == name)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Skill]:
        stmt = select(Skill)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_by_ids(self, ids: Sequence[int]) -> Sequence[Skill]:
        """Возвращает форматы работы по списку ID."""
        if not ids:
            return []

        stmt = select(Skill).where(Skill.id.in_(ids))
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def filter_by_category_id(self, category_id: int) -> Sequence[Skill]:
        stmt = select(Skill).where(Skill.category_id == category_id)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def add(self, skill: Skill) -> Skill:
        self._session.add(skill)
        await self._session.flush()
        await self._session.refresh(skill)

        return skill
