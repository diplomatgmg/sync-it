from enum import StrEnum


__all__ = [
    "GradeEnum",
    "ProfessionEnum",
    "WorkFormatEnum",
]


class GradeEnum(StrEnum):
    UNKNOWN = "Неизвестно"
    INTERN = "Стажер"
    JUNIOR = "Junior"
    JUNIOR_MIDDLE = "Junior/Middle"
    MIDDLE = "Middle"
    MIDDLE_SENIOR = "Middle/Senior"
    SENIOR = "Senior"
    SENIOR_LEAD = "Senior/Lead"
    LEAD = "Lead"


class WorkFormatEnum(StrEnum):
    REMOTE = "Удаленная работа"
    HYBRID = "Гибридная работа"
    OFFICE = "Офисная работа"


class ProfessionEnum(StrEnum):
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
