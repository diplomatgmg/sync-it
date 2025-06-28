from enum import StrEnum
from typing import Self, TypeVar


__all__ = [
    "GradeEnum",
    "ProfessionEnum",
    "WorkFormatEnum",
]


T = TypeVar("T", bound="BaseEnum")


class BaseEnum(StrEnum):
    @classmethod
    def values(cls, *, lower: bool = False) -> list[str]:
        """Возвращает список значений Enum."""
        return [v.value.lower() if lower else v.value for v in cls]

    @classmethod
    def get_safe(cls, label: str) -> Self | None:
        """Возвращает элемент Enum по строковому значению, с игнорированием регистра."""
        for member in cls:
            if member.value.lower() == label.lower():
                return member
        return None


class WorkFormatEnum(BaseEnum):
    UNKNOWN = "Неизвестно"
    REMOTE = "Удаленка"
    HYBRID = "Гибрид"
    OFFICE = "Офис"


class ProfessionEnum(BaseEnum):
    UNKNOWN = "Неизвестно"
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    PYTHON_DEVELOPER = "Python developer"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    TECH_LEAD = "Tech Lead"


class GradeEnum(BaseEnum):
    UNKNOWN = "Неизвестно"
    INTERN = "Стажер"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"
