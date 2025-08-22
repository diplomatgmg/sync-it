from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.main import MenuActionEnum, MenuCallback
from callbacks.vacancy import VacancyActionEnum, VacancyCallback


__all__ = [
    "main_keyboard",
    "main_menu_keyboard",
]


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для возврата в главное меню."""
    buttons = [
        [
            InlineKeyboardButton(
                text="🏠 В меню",
                callback_data=MenuCallback(action=MenuActionEnum.MAIN).pack(),
            ),
        ],
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главном меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="📋 Вакансии",
                callback_data=VacancyCallback(action=VacancyActionEnum.SHOW_VACANCY).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Обновить предпочтения",
                callback_data=MenuCallback(action=MenuActionEnum.PREFERENCES).pack(),
            ),
        ],
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()
