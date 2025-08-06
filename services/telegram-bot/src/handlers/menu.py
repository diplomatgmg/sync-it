from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.main import MenuActionEnum, MenuCallback
from clients.vacancy import vacancy_client
from keyboard.inline.main import main_menu_keyboard
from keyboard.inline.preferences import preferences_keyboard
from utils.formatters import format_publication_time
from utils.message import safe_edit_message


__all__ = ["router"]


router = Router(name=MenuCallback.__prefix__)


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.PREFERENCES))
async def handle_preferences(callback: CallbackQuery) -> None:
    await safe_edit_message(callback, text="⚙️ Выберите предпочтения", reply_markup=preferences_keyboard())


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.VACANCIES))
async def handle_vacancies(callback: CallbackQuery) -> None:
    vacancies = await vacancy_client.get_filtered()

    if not vacancies:
        await safe_edit_message(
            callback,
            text="К сожалению, доступных вакансий нет.\nИзмените предпочтения или загляните сюда позже 😉",
            reply_markup=main_menu_keyboard(),
        )
        return

    vacancy = vacancies[0]

    vacancy_text = f"<b>Должность:</b> {vacancy.profession.name if vacancy.profession else 'Неизвестно'}\n"

    if vacancy.company_name:
        vacancy_text += f"<b>Компания:</b> {vacancy.company_name}\n"
    if vacancy.grades:
        grade_names = [grade.name for grade in vacancy.grades]
        vacancy_text += f"<b>Грейд:</b> {', '.join(grade_names)}\n"
    if vacancy.work_formats:
        work_format_names = [work_format.name for work_format in vacancy.work_formats]
        vacancy_text += f"<b>Формат работы:</b> {', '.join(work_format_names)}\n"
    if vacancy.workplace_description:
        vacancy_text += f"\n<b>О месте работы:</b>\n{vacancy.workplace_description}\n"
    if vacancy.responsibilities:
        vacancy_text += f"\n<b>Обязанности:</b>\n{vacancy.responsibilities}\n"
    if vacancy.requirements:
        vacancy_text += f"\n<b>Требования:</b>\n{vacancy.requirements}\n"
    if vacancy.conditions:
        vacancy_text += f"\n<b>Условия:</b>\n{vacancy.conditions}\n"

    vacancy_text += f"\n<b>Дата публикации:</b> {format_publication_time(vacancy.published_at)}\n"
    vacancy_text += f"<b>Ссылка:</b> <a href='{vacancy.link}'>{vacancy.link}</a>"

    await safe_edit_message(
        callback,
        text=vacancy_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
