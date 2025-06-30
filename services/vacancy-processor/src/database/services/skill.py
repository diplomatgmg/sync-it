from collections.abc import Sequence

from database.models import Skill, SkillCategory
from database.models.enums import SkillCategoryEnum, SkillEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = [
    "SkillCategoryService",
    "SkillService",
]


class SkillCategoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_categories(self) -> Sequence[SkillCategory]:
        stmt = select(SkillCategory)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_category_by_name(self, name: SkillCategoryEnum) -> SkillCategory:
        stmt = select(SkillCategory).where(SkillCategory.name == name)
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def add_category(self, category: SkillCategoryEnum) -> SkillCategory:
        category_model = SkillCategory(name=category)

        self.session.add(category_model)
        await self.session.commit()
        await self.session.refresh(category_model)

        return category_model


class SkillService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_skills(self) -> Sequence[Skill]:
        stmt = select(Skill)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def add_skill(self, skill: SkillEnum, category_id: int) -> Skill:
        skill_model = Skill(name=skill, category_id=category_id)

        self.session.add(skill_model)
        await self.session.commit()
        await self.session.refresh(skill_model)

        return skill_model
