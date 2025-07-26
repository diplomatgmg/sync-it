from typing import cast

from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.preference import PreferenceActionEnum, PreferenceCallback
from clients import GradeClient, ProfessionClient, WorkFormatClient
from common.logger import get_logger
from database.models.enums import PreferenceCategoryCodeEnum
from keyboard.inline.preferences import options_keyboard
from repositories import UserPreferenceRepository, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from utils.clients import ClientType, get_client
from utils.message import get_message, safe_edit_message

from services import UserPreferenceService, UserService


__all__ = ["router"]


logger = get_logger(__name__)


router = Router(name=PreferenceCallback.__prefix__)


async def handle_show_options(
    query: CallbackQuery,
    session: AsyncSession,
    category_code: PreferenceCategoryCodeEnum,
    client_class: ClientType,
    message_text: str,
) -> None:
    async with client_class() as client:
        options = await client.get_all()

    repo = UserRepository(session)
    service = UserService(repo)
    user = await service.get(query.from_user.id, with_preferences=True)

    await safe_edit_message(
        query,
        text=message_text,
        reply_markup=options_keyboard(category_code, options, user),
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_WORK_FORMATS))
async def handle_work_format(query: CallbackQuery, session: AsyncSession) -> None:
    await handle_show_options(
        query,
        session,
        PreferenceCategoryCodeEnum.WORK_FORMAT,
        WorkFormatClient,
        "Выберите формат работы:",
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_GRADES))
async def handle_grade(query: CallbackQuery, session: AsyncSession) -> None:
    await handle_show_options(
        query,
        session,
        PreferenceCategoryCodeEnum.GRADE,
        GradeClient,
        "Выберите грейд:",
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_PROFESSIONS))
async def handle_profession(query: CallbackQuery, session: AsyncSession) -> None:
    await handle_show_options(
        query,
        session,
        PreferenceCategoryCodeEnum.PROFESSION,
        ProfessionClient,
        "Выберите направление:",
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SELECT_OPTION))
async def handle_select_option(
    callback: CallbackQuery,
    callback_data: PreferenceCallback,
    session: AsyncSession,
) -> None:
    """Обрабатывает выбор/снятие выбора опции предпочтения."""
    category_code = cast("PreferenceCategoryCodeEnum", callback_data.category_code)
    item_id = cast("int", callback_data.item_id)

    client_class = get_client(category_code)

    item_name = ""
    async with client_class() as api_client:
        options = await api_client.get_all()
        for option in options:
            if option.id == item_id:
                item_name = option.name
                break

    if not item_name:
        await callback.answer("Ошибка: опция не найдена.", show_alert=True)
        return

    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    user = await user_service.get(callback.from_user.id, with_preferences=True)

    preference_repo = UserPreferenceRepository(session)
    preference_service = UserPreferenceService(preference_repo)
    await preference_service.toggle_preference(user, category_code, item_id, item_name)

    await session.commit()
    await session.refresh(user, attribute_names=["preferences"])

    message = await get_message(callback)

    await safe_edit_message(
        callback,
        text=message.text or "Выберите опцию:",
        reply_markup=options_keyboard(category_code, options, user),
        try_answer=True,
    )
