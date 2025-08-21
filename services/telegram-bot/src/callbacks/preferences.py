from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "PreferencesActionEnum",
    "PreferencesCallback",
]


class PreferencesActionEnum(StrEnum):
    UPDATE_PREFERENCES = "update_preferences"


class PreferencesCallback(CallbackData, prefix="preferences"):
    action: PreferencesActionEnum
