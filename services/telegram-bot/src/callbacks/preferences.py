from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from database.models.enums import PreferenceCategoryCodeEnum


__all__ = [
    "PreferencesActionEnum",
    "PreferencesCallback",
]


class PreferencesActionEnum(StrEnum):
    SHOW_GRADES = PreferenceCategoryCodeEnum.GRADE
    SHOW_PROFESSIONS = PreferenceCategoryCodeEnum.PROFESSION
    SHOW_WORK_FORMATS = PreferenceCategoryCodeEnum.WORK_FORMAT

    SELECT_OPTION = "select_option"


class PreferencesCallback(CallbackData, prefix="preferences"):
    action: PreferencesActionEnum

    # fixme зачем category_code, если уже есть action?
    category_code: str | None = None
    item_id: int | None = None
