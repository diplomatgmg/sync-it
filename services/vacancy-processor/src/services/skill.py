from collections.abc import Sequence

from database.models import Skill, SkillCategory
from database.models.enums import SkillCategoryEnum, SkillEnum
from repositories import SkillCategoryRepository, SkillRepository


__all__ = ["SkillCategoryService", "SkillService"]


class SkillCategoryService:
    """Сервис для бизнес-операций с категориями навыков."""

    def __init__(self, repo: SkillCategoryRepository) -> None:
        self.repo = repo

    async def get_category_by_name(self, name: SkillCategoryEnum) -> SkillCategory | None:
        return await self.repo.get_by_name(name)

    async def get_categories(self) -> Sequence[SkillCategory]:
        return await self.repo.get_all()

    async def add_category(self, category: SkillCategoryEnum) -> SkillCategory:
        category_model = SkillCategory(name=category)
        self.repo.add(category_model)
        return category_model


class SkillService:
    """Сервис для бизнес-операций с навыками."""

    def __init__(self, repo: SkillRepository) -> None:
        self.repo = repo

    async def get_skill_by_name(self, name: SkillEnum) -> Skill | None:
        return await self.repo.get_by_name(name)

    async def get_skills(self) -> Sequence[Skill]:
        return await self.repo.get_all()

    async def add_skill(self, skill: SkillEnum, category_id: int) -> Skill:
        skill_model = Skill(name=skill, category_id=category_id)
        self.repo.add(skill_model)
        return skill_model
