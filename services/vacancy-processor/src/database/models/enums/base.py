from enum import StrEnum
from typing import Any, Self


__all__ = ["BaseAliasEnum"]


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

        if getattr(cls, "__validate_ordering__", False):
            cls._check_members_order()

    @classmethod
    def get_safe(cls, label: str) -> Self | None:
        """Возвращает элемент Enum по строковому значению или алиасу."""
        for member in cls:
            if label.lower() in member.aliases:
                return member

        return None

    @classmethod
    def _check_members_order(cls) -> None:
        """Проверяет, что элементы перечисления отсортированы по значению."""
        members = [item for item in cls.__members__.items() if item[1] != cls.UNKNOWN]  # type: ignore[attr-defined]
        sorted_members = sorted(members, key=lambda item: item[1].value.casefold())

        if members != sorted_members:
            # Находим первый элемент, который нарушает порядок
            for i, ((name_original, value_original), (name_sorted, value_sorted)) in enumerate(
                zip(members, sorted_members, strict=True)
            ):
                if (name_original, value_original) != (name_sorted, value_sorted):
                    original_list = [member[0] for member in members]
                    sorted_list = [member[0] for member in sorted_members]
                    raise ValueError(
                        f"Ordering error in {cls.__name__}: member '{name_original}' is out of order."
                        f"\nExpected order: ... {sorted_list[i - 1]}, {sorted_list[i]}, {sorted_list[i + 1]} ..."
                        f"\nActual order: ... {original_list[i - 1]}, {original_list[i]}, {original_list[i + 1]} ..."
                    )
