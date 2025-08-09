from enum import StrEnum


__all__ = ["PreferenceCategoryCodeEnum"]


class PreferenceCategoryCodeEnum(StrEnum):
    PROFESSION = "profession"
    SKILL_CATEGORY = "skill_category"
    SKILL = "skill"
    GRADE = "grade"
    WORK_FORMAT = "work_format"
