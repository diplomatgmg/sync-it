from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "SkillActionEnum",
    "SkillCallback",
]


class SkillActionEnum(StrEnum):
    TOGGLE_SKILLS = "toggle_skill"
    UPDATE_SKILLS = "update_skills"


class SkillCallback(CallbackData, prefix="preferences"):
    action: SkillActionEnum
