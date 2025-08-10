from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.main import MenuActionEnum, MenuCallback
from callbacks.preference import PreferenceActionEnum, PreferenceCallback
from database.models import User
from database.models.enums import PreferenceCategoryCodeEnum
from schemas import Grade, Profession, Skill, SkillCategory, WorkFormat


__all__ = [
    "options_keyboard",
    "preferences_keyboard",
    "skill_category_keyboard",
]


def preferences_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🎯 Направление",
                callback_data=PreferenceCallback(action=PreferenceActionEnum.SHOW_PROFESSIONS).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🛠️ Навыки",
                callback_data=PreferenceCallback(action=PreferenceActionEnum.SHOW_SKILL_CATEGORIES).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎓 Грейд",
                callback_data=PreferenceCallback(action=PreferenceActionEnum.SHOW_GRADES).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="💻 Формат работы",
                callback_data=PreferenceCallback(action=PreferenceActionEnum.SHOW_WORK_FORMATS).pack(),
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


def options_keyboard(
    category_code: PreferenceCategoryCodeEnum,
    options: Sequence[Grade | Profession | WorkFormat | Skill | SkillCategory],
    user: User,
    # Архитектурная ошибка. Параметра не должно тут быть.
    skill_category_id: int | None = None,
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
            callback_data=PreferenceCallback(
                action=PreferenceActionEnum.SELECT_OPTION,
                category_code=category_code,
                item_id=option.id,
                skill_category_id=skill_category_id,
            ),
        )

    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(
            text="⬅️ К предпочтениям",
            callback_data=MenuCallback(action=MenuActionEnum.PREFERENCES).pack(),
        )
    )
    return builder.as_markup()


def skill_category_keyboard(categories: Sequence[SkillCategory]) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с опциями для выбора категории навыков."""
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(
            text=category.name,
            callback_data=PreferenceCallback(
                action=PreferenceActionEnum.SHOW_SKILLS,
                category_code=PreferenceCategoryCodeEnum.SKILL,
                item_id=category.id,
                skill_category_id=category.id,
            ),
        )

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

    builder.adjust(1)

    return builder.as_markup()
