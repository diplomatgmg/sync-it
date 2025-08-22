from database.models.enums import BaseAliasEnum


__all__ = ["GradeEnum"]


class GradeEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    INTERN = "Стажер"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"
