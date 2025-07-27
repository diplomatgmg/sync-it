from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.main import MenuActionEnum, MenuCallback
from clients.vacancy import vacancy_client
from keyboard.inline.main import main_menu_keyboard
from keyboard.inline.preferences import preferences_keyboard
from utils.message import safe_edit_message


__all__ = ["router"]


router = Router(name=MenuCallback.__prefix__)


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.PREFERENCES))
async def handle_preferences(callback: CallbackQuery) -> None:
    await safe_edit_message(callback, text="⚙️ Выберите предпочтения", reply_markup=preferences_keyboard())


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.VACANCIES))
async def handle_vacancies(callback: CallbackQuery) -> None:
    vacancies = await vacancy_client.get_filtered()

    # FIXME заглушка
    vacancies_text = "\n".join([f"👉 {vacancy.link}" for vacancy in vacancies])[:1024]

    await safe_edit_message(
        callback,
        text=f"👨‍💻 Доступные вакансии:\n{vacancies_text}",
        reply_markup=main_menu_keyboard(),
    )
