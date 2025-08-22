from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from callbacks.preferences import PreferencesActionEnum, PreferencesCallback
from commands import BotCommandEnum
from common.logger import get_logger
from core.loader import bot
from keyboard.inline.main import main_menu_keyboard
from schemas.user import UserRead
from states import PreferencesState
from tasks import process_resume
from tasks.schemas import FileResumePayloadSchema, TextResumePayloadSchema
from utils.message import safe_edit_message
from utils.readers.enums import SupportedReaderExtensionsEnum


__all__ = ()

logger = get_logger(__name__)


router = Router(name=BotCommandEnum.UPDATE_PREFERENCES)


MAX_FILE_SIZE = 5 * 1024 * 1024  # 1 MB
MAX_MESSAGE_LENGTH = 4096


update_preferences_text = (
    "Пришлите информацию, где есть ваши навыки одним из способов:\n"
    "\t- Текстом (до 4096 символов)\n"
    f"\t- Файлом в формате: {', '.join(SupportedReaderExtensionsEnum)} (до {MAX_FILE_SIZE // 1024 // 1024} МБ)\n"
)


@router.message(Command(BotCommandEnum.UPDATE_PREFERENCES))
async def handle_update_preferences_command(message: Message, state: FSMContext) -> None:
    await update_preferences(message, state)


@router.callback_query(PreferencesCallback.filter(F.action == PreferencesActionEnum.UPDATE_PREFERENCES))
async def handle_update_preferences_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await update_preferences(callback, state)


async def update_preferences(entity: CallbackQuery | Message, state: FSMContext) -> None:
    await safe_edit_message(
        entity,
        text=update_preferences_text,
        reply_markup=main_menu_keyboard(),
    )
    await state.set_state(PreferencesState.waiting_for_data)


@router.message(PreferencesState.waiting_for_data)
async def handle_resume_input(message: Message, state: FSMContext, user: UserRead) -> None:  # noqa: PLR0911
    resume_payload: TextResumePayloadSchema | FileResumePayloadSchema

    if text := message.text:
        if len(text) > MAX_MESSAGE_LENGTH:
            await message.reply(
                f"⚠️ Текст слишком длинный, попробуйте сократить его.\n\n{update_preferences_text}",
                reply_markup=main_menu_keyboard(),
            )
            return
        resume_payload = TextResumePayloadSchema(text=text)
    elif document := message.document:
        file_suffix = Path(document.file_name or "").suffix
        if not file_suffix:
            await message.reply(
                f"⚠️ Не удалось определить формат файла.\n\n{update_preferences_text}",
                reply_markup=main_menu_keyboard(),
            )
            return

        if file_suffix not in SupportedReaderExtensionsEnum:
            await message.reply(
                f"⚠️ Неподдерживаемый формат: {file_suffix}\n\n{update_preferences_text}",
                reply_markup=main_menu_keyboard(),
            )
            return

        if not document.file_size:
            logger.warning(
                "File size is not available for message: %s",
                message.model_dump(exclude_none=True),
            )
            await message.reply(
                f"❌ Произошла ошибка. Попробуйте позже.\n\n{update_preferences_text}",
                reply_markup=main_menu_keyboard(),
            )
            return

        if document.file_size > MAX_FILE_SIZE:
            await message.reply(
                f"⚠️ Файл должен быть меньше {MAX_FILE_SIZE // 1024 // 1024} МБ.",
                reply_markup=main_menu_keyboard(),
            )
            return

        file = await bot.get_file(document.file_id)
        if not file.file_path:
            logger.warning(
                "File path is not available for message: %s",
                message.model_dump(exclude_none=True),
            )
            await message.reply(
                f"❌ Произошла ошибка. Попробуйте позже.\n\n{update_preferences_text}",
                reply_markup=main_menu_keyboard(),
            )
            return

        resume_payload = FileResumePayloadSchema(file_path=file.file_path, suffix=file_suffix)
    else:
        await message.reply(
            f"🤔 Вы прислали что-то не понятное.\n\n{update_preferences_text}",
            reply_markup=main_menu_keyboard(),
        )
        return

    await message.answer(
        "ℹ️ Начинаю извлечение навыков из текста.\nПожалуйста, подождите, это может занять некоторое время.",
    )

    process_resume.delay(user.id, message.chat.id, resume_payload.model_dump())
    await state.clear()
