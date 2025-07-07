from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "PreferencesActionEnum",
    "PreferencesCallback",
]


class PreferencesActionEnum(StrEnum):
    GRADE = "grade"
    PROFESSION = "profession"
    WORK_FORMAT = "work_format"


class PreferencesCallback(CallbackData, prefix="preferences"):
    action: PreferencesActionEnum
