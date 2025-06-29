from enum import StrEnum
from typing import Self, TypeVar


__all__ = [
    "BaseEnum",
    "CurrencyEnum",
    "GradeEnum",
    "ProfessionEnum",
    "WorkFormatEnum",
]


T = TypeVar("T", bound="BaseEnum")


class BaseEnum(StrEnum):
    @classmethod
    def get_safe(cls, label: str) -> Self | None:
        """Возвращает элемент Enum по строковому значению, с игнорированием регистра."""
        for member in cls:
            if member.value.lower() == label.lower():
                return member
        return None


class WorkFormatEnum(BaseEnum):
    REMOTE = "Удаленка"
    HYBRID = "Гибрид"
    OFFICE = "Офис"


class ProfessionEnum(BaseEnum):
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    PYTHON_DEVELOPER = "Python developer"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    TECH_LEAD = "Tech Lead"


class GradeEnum(BaseEnum):
    INTERN = "Стажер"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"


class CurrencyEnum(BaseEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
