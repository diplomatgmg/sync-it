from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "MenuActionEnum",
    "MenuCallback",
]


class MenuActionEnum(StrEnum):
    MAIN = "main"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuActionEnum
