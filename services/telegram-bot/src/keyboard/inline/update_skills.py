from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.main import MenuActionEnum, MenuCallback
from callbacks.vacancy import VacancyActionEnum, VacancyCallback


__all__ = ["update_skills_keyboard"]


def update_skills_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для обновленных навыков."""
    buttons = [
        [
            InlineKeyboardButton(
                text="📋 Вакансии",
                callback_data=VacancyCallback(action=VacancyActionEnum.SHOW_VACANCY).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🏠 В меню",
                callback_data=MenuCallback(action=MenuActionEnum.MAIN).pack(),
            ),
        ],
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()
