from common.logger import get_logger
from database.enums import ProfessionEnum


__all__ = ["normalize_profession"]


logger = get_logger(__name__)


def normalize_profession(profession: str) -> ProfessionEnum | None:
    profession = profession.lower().strip()

    if profession in ignore_professions:
        return None

    for profession_enum, aliases in professions_map.items():
        if profession in aliases:
            return profession_enum

    logger.warning("Unknown profession '%s'", profession)
    return None


professions_map = {
    ProfessionEnum.PYTHON_DEVELOPER: ("python developer",),
    ProfessionEnum.BACKEND: ("backend developer",),
    ProfessionEnum.FRONTEND: ("frontend developer",),
    ProfessionEnum.FULLSTACK: ("fullstack developer",),
    ProfessionEnum.DATA_ENGINEER: ("data engineer",),
    ProfessionEnum.DATA_SCIENCE: ("data science",),
    ProfessionEnum.TECH_LEAD: ("it lead", "tech lead"),
}

ignore_professions: set[str] = {
    "iquantitative developer",
}
