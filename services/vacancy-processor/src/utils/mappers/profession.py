from common.logger import get_logger
from database.models.enums import ProfessionEnum


__all__ = ["map_to_profession_enum"]


logger = get_logger(__name__)


def map_to_profession_enum(profession: str) -> ProfessionEnum | None:
    profession = profession.lower().strip()

    if profession in ignore_professions:
        return None

    for profession_enum, aliases in professions_map.items():
        if profession in aliases:
            return profession_enum

    return None


professions_map = {
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
