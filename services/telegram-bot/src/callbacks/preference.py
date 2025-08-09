from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from database.models.enums import PreferenceCategoryCodeEnum


__all__ = [
    "PreferenceActionEnum",
    "PreferenceCallback",
]


class PreferenceActionEnum(StrEnum):
    SHOW_GRADES = "show_grades"
    SHOW_PROFESSIONS = "show_professions"
    SHOW_WORK_FORMATS = "show_work_formats"
    SHOW_SKILL_CATEGORIES = "show_skill_categories"
    SHOW_SKILLS = "show_skills"

    SELECT_OPTION = "select_option"


class PreferenceCallback(CallbackData, prefix="preferences"):
    action: PreferenceActionEnum

    category_code: PreferenceCategoryCodeEnum | None = None
    item_id: int | None = None

    # Костылище. Категория навыков имеет другую структуру, по сравнения с грейдами, профессиями, форматами работы...
    skill_category_id: int | None = None


# TODO проверить корректрость данных в бд. зарплата от и до. добавить ваюту, поля salary_from, salary_to, currency
