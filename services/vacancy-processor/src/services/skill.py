from common.shared.services.base import BaseUOWService
from database.models import Skill, SkillCategory
from database.models.enums import SkillCategoryEnum, SkillEnum
from schemas.skill import SkillCategoryCreate, SkillCategoryRead, SkillCreate, SkillRead
from unitofwork import UnitOfWork


__all__ = ["SkillCategoryService", "SkillService"]


class SkillCategoryService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций с категориями навыков."""

    async def get_category_by_name(self, name: SkillCategoryEnum) -> SkillCategoryRead | None:
        skill_category = await self._uow.skill_categories.get_by_name(name)

        return SkillCategoryRead.model_validate(skill_category) if skill_category else None

    async def get_categories(self) -> list[SkillCategoryRead]:
        skill_categories = await self._uow.skill_categories.get_all()

        return [SkillCategoryRead.model_validate(c) for c in skill_categories]

    async def add_category(self, category: SkillCategoryCreate) -> SkillCategoryRead:
        skill_category_model = SkillCategory(name=category.name)
        created_skill_category = await self._uow.skill_categories.add(skill_category_model)

        return SkillCategoryRead.model_validate(created_skill_category)


class SkillService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций с навыками."""

    async def get_skill_by_name(self, name: SkillEnum) -> SkillRead | None:
        skill = await self._uow.skills.get_by_name(name)

        return SkillRead.model_validate(skill) if skill else None

    async def get_skills(self, category_id: int | None = None) -> list[SkillRead]:
        if category_id:
            skills = await self._uow.skills.filter_by_category_id(category_id)
        else:
            skills = await self._uow.skills.get_all()

        return [SkillRead.model_validate(s) for s in skills]

    async def add_skill(self, skill: SkillCreate) -> SkillRead:
        skill_model = Skill(name=skill.name, category_id=skill.category_id)
        created_skill = await self._uow.skills.add(skill_model)

        return SkillRead.model_validate(created_skill)
