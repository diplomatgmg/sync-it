from typing import TypeVar

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.main import MenuActionEnum, MenuCallback
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback
from clients.schemas import GradeSchema, ProfessionSchema, SkillSchema, WorkFormatSchema
from database.models.enums import PreferencesCategoryCodeEnum
from schemas.user import UserWithPreferences


__all__ = [
    "options_keyboard",
    "preferences_keyboard",
]


def preferences_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🎯 Направление",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.SHOW_PROFESSIONS).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎓 Грейд",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.SHOW_GRADES).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="💻 Формат работы",
                callback_data=PreferencesCallback(action=PreferencesActionEnum.SHOW_WORK_FORMATS).pack(),
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


OptionsType = TypeVar("OptionsType", GradeSchema, ProfessionSchema, WorkFormatSchema, SkillSchema)


def options_keyboard[OptionsType: (GradeSchema, ProfessionSchema, WorkFormatSchema, SkillSchema)](
    category_code: PreferencesCategoryCodeEnum,
    options: list[OptionsType],
    user: UserWithPreferences,
) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с опциями для выбора (грейды, профессии и т.д.)."""
    builder = InlineKeyboardBuilder()

    selected_item_ids = {pref.item_id for pref in user.preferences if pref.category_code == category_code}

    for option in options:
        button_text = option.name

        is_selected = option.id in selected_item_ids
        if is_selected:
            button_text = f"✅ {button_text}"

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
            text="⬅️ К предпочтениям",
            callback_data=MenuCallback(action=MenuActionEnum.PREFERENCES).pack(),
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="🏠 В меню",
            callback_data=MenuCallback(action=MenuActionEnum.MAIN).pack(),
        )
    )

    return builder.as_markup()
