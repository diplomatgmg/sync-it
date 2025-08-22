from database.models.enums import BaseAliasEnum


__all__ = ["WorkFormatEnum"]


class WorkFormatEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    REMOTE = "Удаленка"
    HYBRID = "Гибрид"
    OFFICE = "Офис"
