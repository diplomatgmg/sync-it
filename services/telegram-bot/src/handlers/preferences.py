import asyncio

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback
from clients import grade_client, profession_client, work_format_client
from common.logger import get_logger
from database.models.enums import PreferencesCategoryCodeEnum
from handlers.skills import update_skills
from keyboard.inline.main import main_menu_keyboard
from keyboard.inline.preferences import options_keyboard
from schemas.user_preference import UserPreferenceCreate
from services.user import UserService
from states import PreferencesState
from unitofwork import UnitOfWork
from utils.clients import ClientType, get_client
from utils.message import get_message, safe_edit_message

from services import UserPreferenceService


__all__ = ["router"]


logger = get_logger(__name__)


router = Router(name=PreferencesCallback.__prefix__)


async def handle_show_options(
    query: CallbackQuery,
    user_service: UserService,
    category_code: PreferencesCategoryCodeEnum,
    client: ClientType,
    message_text: str,
) -> None:
    options = await client.get_all()

    user = await user_service.get_by_telegram_id(query.from_user.id, with_preferences=True)

    await safe_edit_message(
        query,
        text=message_text,
        reply_markup=options_keyboard(category_code, options, user),
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SHOW_PROFESSIONS))
async def handle_profession(query: CallbackQuery, user_service: UserService) -> None:
    await handle_show_options(
        query,
        user_service,
        PreferencesCategoryCodeEnum.PROFESSION,
        profession_client,
        "Выберите направление:",
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SHOW_WORK_FORMATS))
async def handle_work_format(query: CallbackQuery, user_service: UserService) -> None:
    await handle_show_options(
        query,
        user_service,
        PreferencesCategoryCodeEnum.WORK_FORMAT,
        work_format_client,
        "Выберите формат работы:",
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SHOW_GRADES))
async def handle_grade(query: CallbackQuery, user_service: UserService) -> None:
    await handle_show_options(
        query,
        user_service,
        PreferencesCategoryCodeEnum.GRADE,
        grade_client,
        "Выберите грейд:",
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SELECT_OPTION))
async def handle_select_option(
    callback: CallbackQuery,
    callback_data: PreferencesCallback,
    user_service: UserService,
    user_preferences_service: UserPreferenceService,
    uow: UnitOfWork,
) -> None:
    """Обрабатывает выбор/снятие выбора опции предпочтения."""
    category_code = callback_data.category_code
    item_id = callback_data.item_id
    if not category_code or not item_id:
        logger.error("Category code or item is empty. Callback data: %s", callback_data)
        await callback.answer("Внутренняя ошибка. Опция не найдена.", show_alert=True)
        return

    client = get_client(category_code)
    options = await client.get_all()

    item_name = ""
    for option in options:
        if option.id == item_id:
            item_name = option.name
            break

    if not item_name:
        logger.error("Option not found: %s. Options: %s. Callback data: %s", item_id, options, callback_data)
        await callback.answer("Внутренняя ошибка. Опция не найдена.", show_alert=True)
        return

    user = await user_service.get_by_telegram_id(callback.from_user.id, with_preferences=True)
    user_preference_create = UserPreferenceCreate(
        user_id=user.id,
        category_code=category_code,
        item_id=item_id,
        item_name=item_name,
    )

    await user_preferences_service.toggle_preference(user_preference_create)
    await uow.commit()

    user = await user_service.get_by_telegram_id(user.telegram_id, with_preferences=True)

    message = await get_message(callback)

    await safe_edit_message(
        callback,
        text=message.text or "Выберите опцию:",
        reply_markup=options_keyboard(
            category_code,
            options,
            user,
        ),
    )


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.SHOW_SKILLS))
async def handle_show_skills(
    callback: CallbackQuery, user_preferences_service: UserPreferenceService, state: FSMContext
) -> None:
    preferences = await user_preferences_service.filter_by_telegram_id_and_category(
        callback.from_user.id, PreferencesCategoryCodeEnum.SKILL
    )
    if not preferences:
        await safe_edit_message(callback, text="У вас пока нет добавленных навыков. \nПожалуйста, добавьте их.")
        await asyncio.sleep(1)
        await update_skills(callback, state, need_edit=False)
        return

    sorted_preferences = sorted(preferences, key=lambda p: p.item_name.casefold())
    preferences_str = ", ".join(f"<code>{p.item_name}</code>" for p in sorted_preferences)

    await state.set_state(PreferencesState.waiting_toggle_skills)
    await safe_edit_message(
        callback,
        text=(
            "🛠 <b>Ваши навыки</b>:\n"
            f"{preferences_str}\n\n"
            "➕ Чтобы <b>добавить</b> новый навык — просто отправьте его название.\n"
            "➖ Чтобы <b>удалить</b> навык — отправьте его название из списка.\n\n"
            "💡 Навыки помогают подбирать более релевантные вакансии!"
        ),
        reply_markup=main_menu_keyboard(),
        parse_mode=ParseMode.HTML,
    )
