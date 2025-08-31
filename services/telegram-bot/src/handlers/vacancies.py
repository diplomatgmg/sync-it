import asyncio
from collections import defaultdict
from contextlib import suppress

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from callbacks.vacancy import VacancyActionEnum, VacancyCallback
from clients.vacancy import vacancy_client
from common.logger import get_logger
from database.models.enums import PreferencesCategoryCodeEnum
from exceptions import MessageNotModifiedError
from handlers.skills import update_skills
from keyboard.inline.main import main_menu_keyboard
from keyboard.inline.vacancies import vacancies_keyboard
from utils.formatters import format_publication_time
from utils.message import get_message, safe_edit_message

from services import UserService


__all__ = ["router"]


logger = get_logger(__name__)

router = Router(name=VacancyCallback.__prefix__)


@router.callback_query(VacancyCallback.filter(F.action == VacancyActionEnum.SHOW_VACANCY))
async def handle_vacancies(  # noqa: PLR0912 C901 PLR0914 Too complex, too many branches, too many variables
    callback: CallbackQuery, callback_data: VacancyCallback, user_service: UserService, state: FSMContext
) -> None:
    vacancy_id = callback_data.vacancy_id

    user = await user_service.get_by_telegram_id(callback.from_user.id, with_preferences=True)

    categorized_prefs = defaultdict(list)
    for pref in user.preferences:
        categorized_prefs[pref.category_code].append(pref.item_name)

    if not categorized_prefs[PreferencesCategoryCodeEnum.SKILL]:
        message = await get_message(callback)
        await message.answer(
            "Бот ориентирован под выдачу релевантных вакансий, на основе ваших навыков, "
            "но в вашем профиле они отсутствуют.\n\n"
            "Пожалуйста, добавьте навыки, чтобы мы могли подобрать для вас вакансии 😉",
        )
        await asyncio.sleep(2)
        await update_skills(message, state, need_edit=False)
        return

    result = await vacancy_client.get_by_id_with_cursor_pagination(
        vacancy_id=vacancy_id,
        professions=categorized_prefs[PreferencesCategoryCodeEnum.PROFESSION],
        grades=categorized_prefs[PreferencesCategoryCodeEnum.GRADE],
        work_formats=categorized_prefs[PreferencesCategoryCodeEnum.WORK_FORMAT],
        skills=categorized_prefs[PreferencesCategoryCodeEnum.SKILL],
    )
    vacancy, prev_id, next_id = result.vacancy, result.prev_id, result.next_id

    if not vacancy:
        await safe_edit_message(
            callback,
            text="К сожалению, доступных вакансий нет.\nИзмените предпочтения или загляните сюда позже 😉",
            reply_markup=main_menu_keyboard(),
        )
        return

    vacancy_text = f"<i>({vacancy.id})</i>\t"
    vacancy_text += f"<b>Должность:</b> {vacancy.profession.name if vacancy.profession else 'Неизвестно'}\n"

    if vacancy.company_name:
        vacancy_text += f"<b>Компания:</b> {vacancy.company_name}\n"
    if vacancy.grades:
        grade_names = [grade.name for grade in vacancy.grades]
        vacancy_text += f"<b>Грейд:</b> {', '.join(grade_names)}\n"
    if vacancy.salary:
        vacancy_text += f"<b>Зарплата:</b> {vacancy.salary}\n"
    if vacancy.work_formats:
        work_format_names = [work_format.name for work_format in vacancy.work_formats]
        vacancy_text += f"<b>Формат работы:</b> {', '.join(work_format_names)}\n"
    if vacancy.skills:
        user_skills = set(categorized_prefs[PreferencesCategoryCodeEnum.SKILL])
        skills = {s.name for s in vacancy.skills}

        matched = ", ".join(f"<code>{s}</code>" for s in sorted(skills & user_skills))
        unmatched = ", ".join(f"<s>{s}</s>" for s in sorted(skills - user_skills))

        vacancy_text += f"<b>Ключевые навыки:</b> {matched}, {unmatched}\n"
    if vacancy.workplace_description:
        vacancy_text += f"\n<b>О месте работы:</b>\n{vacancy.workplace_description}\n"
    if vacancy.responsibilities:
        vacancy_text += f"\n<b>Обязанности:</b>\n{vacancy.responsibilities}\n"
    if vacancy.requirements:
        vacancy_text += f"\n<b>Требования:</b>\n{vacancy.requirements}\n"
    if vacancy.conditions:
        vacancy_text += f"\n<b>Условия:</b>\n{vacancy.conditions}\n"

    vacancy_text += f"\n<b>Источник: </b>{vacancy.source.humanize()}\n"
    vacancy_text += f"\n<b>Дата публикации:</b> {format_publication_time(vacancy.published_at)}\n"

    max_text_length = 4096
    if len(vacancy_text) > max_text_length:
        vacancy_text = vacancy_text[:max_text_length]
        logger.error("Vacancy text is too long. %s, %s", vacancy.id, vacancy.link)

    with suppress(MessageNotModifiedError):
        await safe_edit_message(
            callback,
            text=vacancy_text,
            reply_markup=vacancies_keyboard(
                vacancy_link=vacancy.link,
                previous_vacancy_id=prev_id,
                next_vacancy_id=next_id,
            ),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    if not vacancy_id:
        await callback.answer("Вакансии актуализированы")
