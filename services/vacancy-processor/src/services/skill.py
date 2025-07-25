from collections.abc import Sequence

from common.shared.services import BaseService
from database.models import Skill, SkillCategory
from database.models.enums import SkillCategoryEnum, SkillEnum
from repositories import SkillCategoryRepository, SkillRepository


__all__ = ["SkillCategoryService", "SkillService"]


class SkillCategoryService(BaseService[SkillCategoryRepository]):
    """Сервис для бизнес-операций с категориями навыков."""

    async def get_category_by_name(self, name: SkillCategoryEnum) -> SkillCategory | None:
        return await self._repo.get_by_name(name)

    async def get_categories(self) -> Sequence[SkillCategory]:
        return await self._repo.get_all()

    async def add_category(self, category: SkillCategoryEnum) -> SkillCategory:
        category_model = SkillCategory(name=category)
        self._repo.add(category_model)
        return category_model


class SkillService(BaseService[SkillRepository]):
    """Сервис для бизнес-операций с навыками."""

    async def get_skill_by_name(self, name: SkillEnum) -> Skill | None:
        return await self._repo.get_by_name(name)

    async def get_skills(self) -> Sequence[Skill]:
        return await self._repo.get_all()

    async def add_skill(self, skill: SkillEnum, category_id: int) -> Skill:
        skill_model = Skill(name=skill, category_id=category_id)
        self._repo.add(skill_model)
        return skill_model
