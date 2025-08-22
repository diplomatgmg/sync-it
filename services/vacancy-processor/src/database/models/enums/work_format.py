from database.models.enums import BaseAliasEnum


__all__ = ["WorkFormatEnum"]


class WorkFormatEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    REMOTE = "Удалёнка", ("удалённо", "удаленная работа", "удалённая работа", "удалено", "удаленка", "удаленна")
    HYBRID = "Гибрид"
    OFFICE = "Офис", ("на месте работодателя",)
