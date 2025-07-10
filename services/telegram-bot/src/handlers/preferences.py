from aiogram import F, Router
from aiogram.types import CallbackQuery

from callbacks.preferences import PreferencesActionEnum, PreferencesCallback


__all__ = ["router"]

from utils.message import safe_edit_message

router = Router(name=PreferencesCallback.__prefix__)


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.WORK_FORMAT))
async def handle_work_format(query: CallbackQuery) -> None:
    await safe_edit_message(query, text="work_format")


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.GRADE))
async def handle_grade(query: CallbackQuery) -> None:
    await safe_edit_message(query, text="grade")


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.PROFESSION))
async def handle_profession(query: CallbackQuery) -> None:
    await safe_edit_message(query, text="profession")
