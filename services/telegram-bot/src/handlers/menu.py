from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from callbacks.main import MenuActionEnum, MenuCallback
from keyboard.inline.preferences import preferences_keyboard
from utils.message import safe_edit_message


__all__ = ["router"]


router = Router(name=MenuCallback.__prefix__)


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.PREFERENCES))
async def handle_preferences(callback: CallbackQuery) -> None:
    await safe_edit_message(callback, text="⚙️ Выберите предпочтения", reply_markup=preferences_keyboard())


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.VACANCIES))
async def handle_vacancies(message: Message) -> None:
    await message.answer(
        "vac",
    )
