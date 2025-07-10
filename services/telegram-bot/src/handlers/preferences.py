from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback
from clients import WorkFormatClient
from keyboard.inline.preferences import work_formats_keyboard
from utils.message import safe_edit_message


__all__ = ["router"]


router = Router(name=PreferencesCallback.__prefix__)


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.WORK_FORMAT))
async def handle_work_format(query: CallbackQuery) -> None:
    async with WorkFormatClient() as wf_client:
        work_formats = await wf_client.get_work_formats()

    await safe_edit_message(query, text="Выберите формат работы", reply_markup=work_formats_keyboard(work_formats))


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.GRADE))
async def handle_grade(query: CallbackQuery) -> None:
    await safe_edit_message(query, text="grade")


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.PROFESSION))
async def handle_profession(query: CallbackQuery) -> None:
    await safe_edit_message(query, text="profession")
