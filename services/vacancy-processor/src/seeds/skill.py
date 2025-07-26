from typing import TYPE_CHECKING, cast

from common.database.engine import get_async_session
from common.logger import get_logger
from repositories import SkillCategoryRepository, SkillRepository
from utils.mappers.skill import skills_map

from services import SkillCategoryService, SkillService


if TYPE_CHECKING:
    from database.models import SkillCategory


__all__ = ["seed_skills"]


logger = get_logger(__name__)


async def seed_skills() -> None:
    logger.debug("Start seeding skill categories")

    async with get_async_session() as session:
        skill_category_repo = SkillCategoryRepository(session)
        skill_repo = SkillRepository(session)

        skill_category_service = SkillCategoryService(skill_category_repo)
        skill_service = SkillService(skill_repo)

        existing_skill_category = await skill_category_service.get_categories()
        existing_skill_category_names = [category.name for category in existing_skill_category]

        existing_skills = await skill_service.get_skills()
        existing_skill_names = [skill.name for skill in existing_skills]

        for category_enum, skills in skills_map.items():
            skill_category: SkillCategory | None = None

            if category_enum not in existing_skill_category_names:
                skill_category = await skill_category_service.add_category(category_enum)
                await session.flush()

            if skill_category is None:
                # Категорию получаем из enum, поэтому всегда будет
                skill_category = cast("SkillCategory", await skill_category_service.get_category_by_name(category_enum))

            for skill_enum in skills:
                if skill_enum not in existing_skill_names:
                    await skill_service.add_skill(skill_enum, skill_category.id)

        await session.commit()

    logger.info("Skills seeded")
