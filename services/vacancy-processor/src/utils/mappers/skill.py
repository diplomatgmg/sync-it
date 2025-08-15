from common.logger import get_logger
from database.models.enums import SkillCategoryEnum, SkillEnum


__all__ = [
    "map_to_skill_category_and_skill_enum",
    "skills_map",
]


logger = get_logger(__name__)


def map_to_skill_category_and_skill_enum(skill: str) -> tuple[SkillCategoryEnum, SkillEnum] | tuple[None, None]:
    skill_lower = skill.lower().strip()

    for skill_category_enum, skills in skills_map.items():
        for skill_enum, aliases in skills.items():
            if skill_lower in aliases:
                return skill_category_enum, skill_enum

    return None, None


skills_map: dict[SkillCategoryEnum, dict[SkillEnum, tuple[str, ...]]] = {
    SkillCategoryEnum.LANGUAGES: {
        SkillEnum.PYTHON: ("python", "python developer"),
        SkillEnum.JAVASCRIPT: ("javascript",),
        SkillEnum.TYPESCRIPT: ("typescript",),
        SkillEnum.HTML: ("html",),
        SkillEnum.CSS: ("css",),
        SkillEnum.SQL: ("sql",),
    },
    SkillCategoryEnum.BACKEND: {
        SkillEnum.DJANGO: ("django",),
        SkillEnum.FLASK: ("flask",),
        SkillEnum.FASTAPI: ("fastapi",),
    },
    SkillCategoryEnum.FRONTEND: {
        SkillEnum.REACT: ("react",),
        SkillEnum.VUE: ("vue",),
        SkillEnum.ANGULAR: ("angular",),
        SkillEnum.SVELTE: ("svelte",),
    },
    SkillCategoryEnum.DEVOPS: {
        SkillEnum.DOCKER: ("docker",),
        SkillEnum.KUBERNETES: ("kubernetes",),
    },
}
