from async_lru import alru_cache
from common.shared.services import BaseUOWService
from database.models import Skill
from database.models.enums import SkillEnum
from schemas.skill import SkillCreate, SkillRead
from unitofwork import UnitOfWork


__all__ = ["SkillService"]


class SkillService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций с навыками."""

    @alru_cache
    async def get_skill_by_name(self, name: SkillEnum) -> SkillRead:
        skill = await self._uow.skills.get_by_name(name)

        return SkillRead.model_validate(skill)

    async def get_skills(self) -> list[SkillRead]:
        skills = await self._uow.skills.get_all()

        return [SkillRead.model_validate(s) for s in skills]

    async def add_skill(self, skill: SkillCreate) -> SkillRead:
        skill_model = Skill(**skill.model_dump())
        created_skill = await self._uow.skills.add(skill_model)

        self.get_skill_by_name.cache_clear()

        return SkillRead.model_validate(created_skill)
