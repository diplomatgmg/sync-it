from aiogram import F, Router
from aiogram.types import Message
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback


__all__ = ["router"]


router = Router(name=PreferencesCallback.__prefix__)


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.WORK_FORMAT))
async def handle_work_format(message: Message) -> None:
    await message.answer(
        "work_format",
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.GRADE))
async def handle_grade(message: Message) -> None:
    await message.answer(
        "grade",
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.PROFESSION))
async def handle_profession(message: Message) -> None:
    await message.answer(
        "profession",
    )
