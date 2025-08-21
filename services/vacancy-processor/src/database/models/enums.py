from enum import StrEnum
from typing import Any, Self, cast


__all__ = [
    "GradeEnum",
    "ProfessionEnum",
    "SkillEnum",
    "SourceEnum",
    "WorkFormatEnum",
]


class BaseAliasEnum(StrEnum):
    aliases: tuple[str, ...]

    def __new__(cls, normalized: str, aliases: tuple[str, ...] = ()) -> Self:
        obj = str.__new__(cls, normalized)
        obj._value_ = normalized
        obj.aliases = (normalized.lower(), *(a.lower() for a in aliases))
        return obj

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Проверяем, что у наследников есть UNKNOWN"""
        super().__init_subclass__(**kwargs)
        if "UNKNOWN" not in cls.__members__:
            raise ValueError(f"{cls.__name__} must define UNKNOWN member")

    def __bool__(self) -> bool:
        """Возвращает True, если элемент не UNKNOWN"""
        return self is not self.UNKNOWN  # type: ignore[attr-defined]

    @classmethod
    def get_safe(cls, label: str) -> Self:
        """Возвращает элемент Enum по строковому значению или алиасу."""
        for member in cls:
            if label.lower() in member.aliases:
                return member

        return cast("Self", cls.UNKNOWN)  # type: ignore[attr-defined]


class SourceEnum(StrEnum):
    TELEGRAM = "telegram"
    HEAD_HUNTER = "head_hunter"


class WorkFormatEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    REMOTE = "Удаленка", ("удалённая", "удаленная")
    HYBRID = "Гибрид"
    OFFICE = "Офис", ("на месте работодателя", "офис")


class ProfessionEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    TECH_LEAD = "Tech Lead"


class GradeEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    INTERN = "Стажер", ("стажёр", "intern")
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"


class SkillEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"

    # <Enum name> = "normalized name", ("alias1", alias 2")
    PYTHON = "Python"
