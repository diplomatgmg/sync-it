from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.noop import NoopActionEnum, NoopCallback
from callbacks.vacancy import VacancyActionEnum, VacancyCallback
from common.shared.schemas import HttpsUrl
from keyboard.buttons import MainMenuInlineKeyboardButton


__all__ = ["vacancies_keyboard"]


def vacancies_keyboard(
    vacancy_link: HttpsUrl,
    previous_vacancy_id: int | None,
    next_vacancy_id: int | None,
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для пагинации списка вакансий и возврата в меню.
    """
    builder = InlineKeyboardBuilder()

    row = []
    if previous_vacancy_id:
        row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=VacancyCallback(
                    action=VacancyActionEnum.SHOW_VACANCY,
                    vacancy_id=previous_vacancy_id,
                ).pack(),
            )
        )
    else:
        row.append(
            InlineKeyboardButton(
                text="❌",
                callback_data=NoopCallback(action=NoopActionEnum.DO_NOTHING).pack(),
            )
        )
    row.append(
        InlineKeyboardButton(
            text="Открыть",
            url=str(vacancy_link),
        )
    )
    if next_vacancy_id:
        row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=VacancyCallback(
                    action=VacancyActionEnum.SHOW_VACANCY,
                    vacancy_id=next_vacancy_id,
                ).pack(),
            )
        )
    else:
        row.append(
            InlineKeyboardButton(
                text="❌",
                callback_data=NoopCallback(action=NoopActionEnum.DO_NOTHING).pack(),
            )
        )
    builder.row(*row)

    builder.row(
        InlineKeyboardButton(
            text="🔄 Обновить",
            callback_data=VacancyCallback(action=VacancyActionEnum.SHOW_VACANCY).pack(),
        )
    )

    builder.row(MainMenuInlineKeyboardButton())

    return builder.as_markup()
