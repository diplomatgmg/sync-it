from typing import cast

from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.preference import PreferenceActionEnum, PreferenceCallback
from clients import BaseClient, GradeClient, ProfessionClient, WorkFormatClient
from common.logger import get_logger
from database.models import User
from database.models.enums import PreferenceCategoryCodeEnum
from keyboard.inline.preferences import options_keyboard
from repositories import UserPreferenceRepository, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from utils.message import safe_edit_message

from services import UserPreferenceService, UserService


__all__ = ["router"]


logger = get_logger(__name__)


router = Router(name=PreferenceCallback.__prefix__)


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_WORK_FORMATS))
async def handle_work_format(query: CallbackQuery, session: AsyncSession) -> None:
    async with WorkFormatClient() as wf_client:
        work_formats = await wf_client.get_work_formats()

    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    user = await user_service.get(query.from_user.id, with_preferences=True)

    await safe_edit_message(
        query,
        text="Выберите формат работы",
        reply_markup=options_keyboard(PreferenceCategoryCodeEnum.WORK_FORMAT, work_formats, user),
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_GRADES))
async def handle_grade(query: CallbackQuery, session: AsyncSession) -> None:
    async with GradeClient() as grade_client:
        grades = await grade_client.get_grades()

    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    user = await user_service.get(query.from_user.id, with_preferences=True)

    await safe_edit_message(
        query,
        text="Выберите грейд",
        reply_markup=options_keyboard(PreferenceCategoryCodeEnum.GRADE, grades, user),
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_PROFESSIONS))
async def handle_profession(query: CallbackQuery, session: AsyncSession) -> None:
    async with ProfessionClient() as prof_client:
        professions = await prof_client.get_professions()

    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    user = await user_service.get(query.from_user.id, with_preferences=True)

    await safe_edit_message(
        query,
        text="Выберите профессию",
        reply_markup=options_keyboard(PreferenceCategoryCodeEnum.PROFESSION, professions, user),
    )


@router.callback_query(
    PreferenceCallback.filter(
        (F.action == PreferenceActionEnum.SELECT_OPTION) & (F.category_code.is_not_none()) & (F.item_id.is_not_none())
    )
)
async def handle_select_option(
    callback: CallbackQuery,
    callback_data: PreferenceCallback,
    user: User,
    session: AsyncSession,
) -> None:
    """Обрабатывает выбор/снятие выбора опции предпочтения."""
    category_code = cast("PreferenceCategoryCodeEnum", callback_data.category_code)
    item_id = cast("int", callback_data.item_id)

    clients: dict[PreferenceCategoryCodeEnum, type[BaseClient]] = {
        PreferenceCategoryCodeEnum.GRADE: GradeClient,
        PreferenceCategoryCodeEnum.PROFESSION: ProfessionClient,
        PreferenceCategoryCodeEnum.WORK_FORMAT: WorkFormatClient,
    }
    getters: dict[PreferenceCategoryCodeEnum, str] = {
        PreferenceCategoryCodeEnum.GRADE: "get_grades",
        PreferenceCategoryCodeEnum.PROFESSION: "get_professions",
        PreferenceCategoryCodeEnum.WORK_FORMAT: "get_work_formats",
    }
    client_class = clients[category_code]
    getter_name = getters[category_code]

    # 2. Находим имя опции, чтобы сохранить его в БД
    item_name = ""
    async with client_class() as api_client:
        getter = getattr(api_client, getter_name)
        options = await getter()
        for option in options:
            if option.id == item_id:
                item_name = option.name
                break

    if not item_name:
        await callback.answer("Ошибка: опция не найдена.", show_alert=True)
        return

    # 3. Переключаем состояние в БД
    repo = UserPreferenceRepository(session)
    service = UserPreferenceService(repo)
    await service.toggle_preference(user, category_code, item_id, item_name)

    # 4. Обновляем клавиатуру, чтобы показать изменения
    await session.refresh(user)  # ОБЯЗАТЕЛЬНО обновляем user, чтобы получить свежие preferences

    # Перерисовываем то же самое меню с обновленными данными
    await safe_edit_message(
        callback,
        text=f"Выберите {category_code}:",
        reply_markup=options_keyboard(category_code, options, user),
    )
