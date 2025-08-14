from enum import StrEnum


__all__ = [
    "CurrencyEnum",
    "GradeEnum",
    "ProfessionEnum",
    "SkillCategoryEnum",
    "SkillEnum",
    "WorkFormatEnum",
]


class WorkFormatEnum(StrEnum):
    REMOTE = "Удаленка"
    HYBRID = "Гибрид"
    OFFICE = "Офис"


class ProfessionEnum(StrEnum):
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    TECH_LEAD = "Tech Lead"


class GradeEnum(StrEnum):
    INTERN = "Стажер"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"


class CurrencyEnum(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class SkillCategoryEnum(StrEnum):
    LANGUAGES = "Языки программирования"
    BACKEND = "Backend"
    FRONTEND = "Frontend"
    DEVOPS = "DevOps"


class SkillEnum(StrEnum):
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
