from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "MenuActionEnum",
    "MenuCallback",
]


class MenuActionEnum(StrEnum):
    MAIN = "main"
    PREFERENCES = "preferences"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuActionEnum
