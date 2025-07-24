from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.main import MenuActionEnum, MenuCallback
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback
from database.models import User
from database.models.enums import PreferenceCategoryCodeEnum
from schemas import Grade, Profession, WorkFormat


__all__ = [
    "options_keyboard",
    "preferences_keyboard",
]


def preferences_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🛠  Профессия",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.SHOW_PROFESSIONS).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎓  Грейд",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.SHOW_GRADES).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="💼  Формат работы",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.SHOW_WORK_FORMATS).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=MenuCallback(action=MenuActionEnum.MAIN).pack(),
            ),
        ],
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()


def options_keyboard(
    category_code: PreferenceCategoryCodeEnum,
    options: Sequence[Grade | Profession | WorkFormat],
    user: User,
) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с опциями для выбора (грейды, профессии и т.д.)."""
    builder = InlineKeyboardBuilder()

    selected_item_ids = {pref.item_id for pref in user.preferences if pref.category_code == category_code}

    for option in options:
        is_selected = option.id in selected_item_ids
        button_text = f"🔶 {option.name}" if is_selected else option.name

        builder.button(
            text=button_text,
            callback_data=PreferencesCallback(
                action=PreferencesActionEnum.SELECT_OPTION,
                category_code=category_code,
                item_id=option.id,
            ),
        )

    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=MenuCallback(action=MenuActionEnum.PREFERENCES).pack(),
        )
    )
    return builder.as_markup()
