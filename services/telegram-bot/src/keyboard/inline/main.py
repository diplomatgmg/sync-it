from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.main import MenuActionEnum, MenuCallback


__all__ = ["main_keyboard"]


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главном меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="📋 Вакансии",
                callback_data=MenuCallback(action=MenuActionEnum.VACANCIES).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⚙️  Предпочтения",
                callback_data=MenuCallback(action=MenuActionEnum.PREFERENCES).pack(),
            ),
        ],
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()
