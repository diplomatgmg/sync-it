from database.models.enums import ProfessionEnum


__all__ = ["map_to_profession_enum"]


def map_to_profession_enum(profession: str) -> ProfessionEnum:
    profession = profession.lower().strip()

    if profession in ignore_professions:
        return ProfessionEnum.UNKNOWN

    profession_enum = ProfessionEnum.get_safe(profession)
    if profession_enum:
        return profession_enum

    for profession_enum, aliases in professions_map.items():
        if profession in aliases:
            return profession_enum

    return ProfessionEnum.UNKNOWN


professions_map: dict[ProfessionEnum, tuple[str, ...]] = {}

ignore_professions: set[str] = {
    "iquantitative developer",
}
