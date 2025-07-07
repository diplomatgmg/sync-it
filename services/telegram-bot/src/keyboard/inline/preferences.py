from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback


__all__ = ["preferences_keyboard"]


def preferences_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🛠  Профессия",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.PROFESSION).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎓  Грейд",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.GRADE).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="💼  Формат работы",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.WORK_FORMAT).pack(),
            ),
        ],
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()
