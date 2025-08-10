from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "VacancyActionEnum",
    "VacancyCallback",
]


class VacancyActionEnum(StrEnum):
    SHOW_VACANCY = "show_vacancy"


class VacancyCallback(CallbackData, prefix="vacancy"):
    action: VacancyActionEnum

    # -1 - самая актуальная на основе предпочтений
    vacancy_id: int = -1
