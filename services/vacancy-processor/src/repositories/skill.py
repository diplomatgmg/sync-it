from collections.abc import Sequence

from database.models import Skill, SkillCategory
from database.models.enums import SkillCategoryEnum, SkillEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["SkillCategoryRepository", "SkillRepository"]


class SkillCategoryRepository:
    """Репозиторий для управления категориями навыков."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, name: SkillCategoryEnum) -> SkillCategory | None:
        stmt = select(SkillCategory).where(SkillCategory.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[SkillCategory]:
        stmt = select(SkillCategory)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def add(self, category_model: SkillCategory) -> None:
        self.session.add(category_model)


class SkillRepository:
    """Репозиторий для управления навыками."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, name: SkillEnum) -> Skill | None:
        stmt = select(Skill).where(Skill.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Skill]:
        stmt = select(Skill)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def add(self, skill_model: Skill) -> None:
        self.session.add(skill_model)
