from enum import StrEnum
from typing import Self, TypeVar


__all__ = [
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
