from common.logger import get_logger
from database.models.enums import SkillEnum
from schemas.skill import SkillCreate
from unitofwork import UnitOfWork

from services import SkillService


__all__ = ["seed_skills"]


logger = get_logger(__name__)


async def seed_skills() -> None:
    logger.debug("Start seeding skill categories")

    async with UnitOfWork() as uow:
        skill_service = SkillService(uow)
        existing_skills = await skill_service.get_skills()
        existing_skill_names = [skill.name for skill in existing_skills]

        for enum_skill in SkillEnum:
            if enum_skill not in existing_skill_names:
                skill = SkillCreate(name=enum_skill)
                await skill_service.add_skill(skill)

        await uow.commit()

    logger.info("Skills seeded")
