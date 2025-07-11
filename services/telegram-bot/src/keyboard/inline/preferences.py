from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.noop import NoopActionEnum, NoopCallback
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback
from schemas import WorkFormat, Grade, Profession

__all__ = [
    "preferences_keyboard",
    "work_formats_keyboard",
]


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


def work_formats_keyboard(work_formats: list[WorkFormat]) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=work_format.name,
                callback_data=NoopCallback(action=NoopActionEnum.DO_NOTHING).pack(),
            ),
        ]
        for work_format in work_formats
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()


def grades_keyboard(grades: list[Grade]) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=grade.name,
                callback_data=NoopCallback(action=NoopActionEnum.DO_NOTHING).pack(),
            ),
        ]
        for grade in grades
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()


def professions_keyboard(professions: list[Profession]) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=profession.name,
                callback_data=NoopCallback(action=NoopActionEnum.DO_NOTHING).pack(),
            ),
        ]
        for profession in professions
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()
