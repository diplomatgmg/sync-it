from typing import cast

from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.preference import PreferenceActionEnum, PreferenceCallback
from clients import grade_client, profession_client, skill_category_client, skill_client, work_format_client
from common.logger import get_logger
from database.models.enums import PreferenceCategoryCodeEnum
from keyboard.inline.preferences import options_keyboard, skill_category_keyboard
from repositories import UserPreferenceRepository, UserRepository
from services.user import UserService
from services.user_preference import UserPreferenceService
from sqlalchemy.ext.asyncio import AsyncSession
from utils.clients import ClientType, get_client
from utils.message import get_message, safe_edit_message


__all__ = ["router"]


logger = get_logger(__name__)


router = Router(name=PreferenceCallback.__prefix__)


async def handle_show_options(
    query: CallbackQuery,
    session: AsyncSession,
    category_code: PreferenceCategoryCodeEnum,
    client: ClientType,
    message_text: str,
) -> None:
    options = await client.get_all()

    repo = UserRepository(session)
    service = UserService(repo)
    user = await service.get(query.from_user.id, with_preferences=True)

    await safe_edit_message(
        query,
        text=message_text,
        reply_markup=options_keyboard(category_code, options, user),
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_PROFESSIONS))
async def handle_profession(query: CallbackQuery, session: AsyncSession) -> None:
    await handle_show_options(
        query,
        session,
        PreferenceCategoryCodeEnum.PROFESSION,
        profession_client,
        "Выберите направление:",
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_WORK_FORMATS))
async def handle_work_format(query: CallbackQuery, session: AsyncSession) -> None:
    await handle_show_options(
        query,
        session,
        PreferenceCategoryCodeEnum.WORK_FORMAT,
        work_format_client,
        "Выберите формат работы:",
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_GRADES))
async def handle_grade(query: CallbackQuery, session: AsyncSession) -> None:
    await handle_show_options(
        query,
        session,
        PreferenceCategoryCodeEnum.GRADE,
        grade_client,
        "Выберите грейд:",
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_SKILL_CATEGORIES))
async def handle_skill_categories(query: CallbackQuery) -> None:
    skill_categories = await skill_category_client.get_all()

    await safe_edit_message(
        query,
        text="Выберите категорию навыков:",
        reply_markup=skill_category_keyboard(skill_categories),
    )


@router.callback_query(PreferenceCallback.filter(F.action == PreferenceActionEnum.SHOW_SKILLS))
async def handle_skills(query: CallbackQuery, callback_data: PreferenceCallback, session: AsyncSession) -> None:
    category_id = callback_data.item_id
    skill_category_id = callback_data.skill_category_id

    skills = await skill_client.get_by_category_id(category_id)

    repo = UserRepository(session)
    service = UserService(repo)
    user = await service.get(query.from_user.id, with_preferences=True)

    await safe_edit_message(
        query,
        text="Выберите навык:",
        reply_markup=options_keyboard(
            PreferenceCategoryCodeEnum.SKILL,
            skills,
            user,
            skill_category_id=skill_category_id,
        ),
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
    # Костыль. Нарушает общую архитектуру.
    skill_category_id = callback_data.skill_category_id

    if category_code == PreferenceCategoryCodeEnum.SKILL:
        if skill_category_id is None:
            logger.error("Skill category id is None")
            await callback.answer("Внутренняя ошибка. Попробуйте позже.", show_alert=True)
            return
        options = await skill_client.get_by_category_id(skill_category_id)
    else:
        client = get_client(category_code)
        options = await client.get_all()

    item_name = ""
    for option in options:
        if option.id == item_id:
            item_name = option.name
            break

    if not item_name:
        logger.error("Option not found: %s. Options: %s", item_id, options)
        await callback.answer("Внутренняя ошибка. Опция не найдена.", show_alert=True)
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
        reply_markup=options_keyboard(
            category_code,
            options,
            user,
            skill_category_id=skill_category_id,
        ),
    )
