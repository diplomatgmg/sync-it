# ruff: noqa: E501
from database.models.enums import BaseAliasEnum


__all__ = ["WorkFormatEnum"]


# fmt: off
class WorkFormatEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    REMOTE = "Удалёнка", ("удалённо", "удаленная работа", "удалённая работа", "удалено", "удаленка", "удаленна", "удалённая")
    HYBRID = "Гибрид"
    OFFICE = "Офис", ("на месте работодателя",)
# fmt: on
