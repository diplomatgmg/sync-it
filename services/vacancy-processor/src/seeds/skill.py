from common.logger import get_logger
from schemas.skill import SkillCategoryCreate, SkillCategoryRead, SkillCreate
from unitofwork import UnitOfWork
from utils.mappers.skill import skills_map

from services import SkillCategoryService, SkillService


__all__ = ["seed_skills"]


logger = get_logger(__name__)


async def seed_skills() -> None:
    logger.debug("Start seeding skill categories")

    async with UnitOfWork() as uow:
        skill_category_service = SkillCategoryService(uow)
        skill_service = SkillService(uow)

        existing_skill_category = await skill_category_service.get_categories()
        existing_skill_category_names = [category.name for category in existing_skill_category]

        existing_skills = await skill_service.get_skills()
        existing_skill_names = [skill.name for skill in existing_skills]

        for skill_category_enum, skills in skills_map.items():
            skill_category_read: SkillCategoryRead | None = None

            if skill_category_enum not in existing_skill_category_names:
                skill_category_create = SkillCategoryCreate(name=skill_category_enum)
                skill_category_read = await skill_category_service.add_category(skill_category_create)

            if not skill_category_read:
                # Категорию получаем из enum, поэтому всегда будет
                skill_category_read = await skill_category_service.get_category_by_name(skill_category_enum)

            for skill_enum in skills:
                if skill_enum not in existing_skill_names:
                    skill = SkillCreate(name=skill_enum, category_id=skill_category_read.id)
                    await skill_service.add_skill(skill)

        await uow.commit()

    logger.info("Skills seeded")
