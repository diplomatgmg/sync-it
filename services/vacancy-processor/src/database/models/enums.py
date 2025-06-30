from enum import StrEnum
from typing import Self, TypeVar


__all__ = [
    "BaseStrEnum",
    "CurrencyEnum",
    "GradeEnum",
    "ProfessionEnum",
    "SkillCategoryEnum",
    "SkillEnum",
    "WorkFormatEnum",
]


T = TypeVar("T", bound="BaseStrEnum")


class BaseStrEnum(StrEnum):
    @classmethod
    def get_safe(cls, label: str) -> Self | None:
        """Возвращает элемент Enum по строковому значению, с игнорированием регистра."""
        for member in cls:
            if member.value.lower() == label.lower():
                return member
        return None


class WorkFormatEnum(BaseStrEnum):
    REMOTE = "Удаленка"
    HYBRID = "Гибрид"
    OFFICE = "Офис"


class ProfessionEnum(BaseStrEnum):
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    PYTHON_DEVELOPER = "Python developer"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    TECH_LEAD = "Tech Lead"


class GradeEnum(BaseStrEnum):
    INTERN = "Стажер"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"


class CurrencyEnum(BaseStrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class SkillCategoryEnum(BaseStrEnum):
    LANGUAGES = "Languages"
    BACKEND = "Backend"
    FRONTEND = "Frontend"
    DEVOPS = "DevOps"


class SkillEnum(BaseStrEnum):
    # Languages
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"
    HTML = "HTML"
    CSS = "CSS"
    SQL = "SQL"

    # Backend
    DJANGO = "Django"
    FLASK = "Flask"
    FASTAPI = "FastAPI"

    # Frontend
    REACT = "React"
    VUE = "Vue"
    ANGULAR = "Angular"
    SVELTE = "Svelte"

    # DevOps
    DOCKER = "Docker"
    KUBERNETES = "Kubernetes"
