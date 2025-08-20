from database.models.enums import ProfessionEnum


__all__ = ["map_to_profession_enum"]


def map_to_profession_enum(profession: str) -> ProfessionEnum:
    profession = profession.lower().strip()

    if profession in ignore_professions:
        return ProfessionEnum.UNKNOWN

    for profession_enum, aliases in professions_map.items():
        if profession in aliases:
            return profession_enum

    return ProfessionEnum.UNKNOWN


professions_map: dict[ProfessionEnum, tuple[str, ...]] = {
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
