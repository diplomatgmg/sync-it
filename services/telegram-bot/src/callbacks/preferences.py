from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from database.models.enums import PreferencesCategoryCodeEnum


__all__ = [
    "PreferencesActionEnum",
    "PreferencesCallback",
]


class PreferencesActionEnum(StrEnum):
    UPDATE_SKILLS = "update_skills"

    SHOW_GRADES = "show_grades"
    SHOW_PROFESSIONS = "show_professions"
    SHOW_WORK_FORMATS = "show_work_formats"

    SELECT_OPTION = "select_option"


class PreferencesCallback(CallbackData, prefix="preferences"):
    action: PreferencesActionEnum

    category_code: PreferencesCategoryCodeEnum | None = None
    item_id: int | None = None
