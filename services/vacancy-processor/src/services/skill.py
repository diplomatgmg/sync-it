from async_lru import alru_cache
from common.shared.services import BaseUOWService
from database.models import Skill, SkillCategory
from database.models.enums import SkillCategoryEnum, SkillEnum
from schemas.skill import SkillCategoryCreate, SkillCategoryRead, SkillCreate, SkillRead
from unitofwork import UnitOfWork


__all__ = ["SkillCategoryService", "SkillService"]


class SkillCategoryService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций с категориями навыков."""

    @alru_cache
    async def get_category_by_name(self, name: SkillCategoryEnum) -> SkillCategoryRead:
        skill_category = await self._uow.skill_categories.get_by_name(name)

        return SkillCategoryRead.model_validate(skill_category)

    async def get_categories(self) -> list[SkillCategoryRead]:
        skill_categories = await self._uow.skill_categories.get_all()

        return [SkillCategoryRead.model_validate(c) for c in skill_categories]

    async def add_category(self, category: SkillCategoryCreate) -> SkillCategoryRead:
        skill_category_model = SkillCategory(**category.model_dump())
        created_skill_category = await self._uow.skill_categories.add(skill_category_model)

        self.get_category_by_name.cache_clear()

        return SkillCategoryRead.model_validate(created_skill_category)


class SkillService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций с навыками."""

    @alru_cache
    async def get_skill_by_name(self, name: SkillEnum) -> SkillRead:
        skill = await self._uow.skills.get_by_name(name)

        return SkillRead.model_validate(skill)

    async def get_skills(self, category_id: int | None = None) -> list[SkillRead]:
        if category_id:
            skills = await self._uow.skills.filter_by_category_id(category_id)
        else:
            skills = await self._uow.skills.get_all()

        return [SkillRead.model_validate(s) for s in skills]

    async def add_skill(self, skill: SkillCreate) -> SkillRead:
        skill_model = Skill(**skill.model_dump())
        created_skill = await self._uow.skills.add(skill_model)

        self.get_skill_by_name.cache_clear()

        return SkillRead.model_validate(created_skill)
