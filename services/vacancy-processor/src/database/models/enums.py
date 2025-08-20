from enum import StrEnum
from typing import Self


__all__ = [
    "GradeEnum",
    "ProfessionEnum",
    "SkillCategoryEnum",
    "SkillEnum",
    "SourceEnum",
    "WorkFormatEnum",
]


class BaseStrEnum(StrEnum):
    @classmethod
    def get_safe(cls, label: str) -> Self | None:
        """Возвращает элемент Enum по строковому значению, с игнорированием регистра."""
        for member in cls:
            if member.value.lower() == label.lower():
                return member
        return None


class SourceEnum(BaseStrEnum):
    TELEGRAM = "telegram"
    HEAD_HUNTER = "head_hunter"


class WorkFormatEnum(BaseStrEnum):
    UNKNOWN = "Неизвестно"
    REMOTE = "Удаленка"
    HYBRID = "Гибрид"
    OFFICE = "Офис"


class ProfessionEnum(BaseStrEnum):
    UNKNOWN = "Неизвестно"
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    TECH_LEAD = "Tech Lead"


class GradeEnum(BaseStrEnum):
    UNKNOWN = "Неизвестно"
    INTERN = "Стажер"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"


class SkillCategoryEnum(BaseStrEnum):
    pass


class SkillEnum(BaseStrEnum):
    pass
