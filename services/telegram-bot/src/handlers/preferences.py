from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback
from clients import GradeClient, ProfessionClient, WorkFormatClient
from database.models import User
from database.models.enums import PreferenceCategoryCodeEnum
from keyboard.inline.preferences import options_keyboard
from utils.message import safe_edit_message


__all__ = ["router"]


router = Router(name=PreferencesCallback.__prefix__)


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SHOW_WORK_FORMATS))
async def handle_work_format(query: CallbackQuery, user: User) -> None:
    async with WorkFormatClient() as wf_client:
        work_formats = await wf_client.get_work_formats()

    await safe_edit_message(
        query,
        text="Выберите формат работы",
        reply_markup=options_keyboard(PreferenceCategoryCodeEnum.WORK_FORMAT, work_formats, user),
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SHOW_GRADES))
async def handle_grade(query: CallbackQuery, user: User) -> None:
    async with GradeClient() as grade_client:
        grades = await grade_client.get_grades()

    await safe_edit_message(
        query,
        text="Выберите грейд",
        reply_markup=options_keyboard(PreferenceCategoryCodeEnum.GRADE, grades, user),
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SHOW_PROFESSIONS))
async def handle_profession(query: CallbackQuery, user: User) -> None:
    async with ProfessionClient() as prof_client:
        professions = await prof_client.get_professions()

    await safe_edit_message(
        query,
        text="Выберите профессию",
        reply_markup=options_keyboard(PreferenceCategoryCodeEnum.PROFESSION, professions, user),
    )
