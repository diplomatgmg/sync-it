from database.models.enums import BaseAliasEnum


__all__ = ["GradeEnum"]


class GradeEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    INTERN = "Стажер", ("trainee",)
    JUNIOR = "Junior", ("junior+",)
    MIDDLE = "Middle", ("middle+", "mid", "средний")
    SENIOR = "Senior"
    LEAD = "Lead"
