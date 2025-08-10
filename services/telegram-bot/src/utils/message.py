from typing import NotRequired, TypedDict, Unpack

from aiogram.client.default import Default
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InaccessibleMessage, InlineKeyboardMarkup, Message
from common.logger import get_logger
from exceptions import MessageNotAvailableError, MessageNotModifiedError


__all__ = [
    "get_message",
    "make_linked",
    "safe_edit_message",
]

logger = get_logger(__name__)


class EditMessageKwargs(TypedDict):
    text: NotRequired[str]
    parse_mode: NotRequired[str | Default | None]
    reply_markup: NotRequired[InlineKeyboardMarkup | None]
    disable_web_page_preview: NotRequired[bool | Default | None]


def make_linked(text: str, link: str | None, *, use_quotes: bool = True) -> str:
    """Возвращает bold текст обернутый в ссылку по возможности"""
    bold_text = f"<b>{text}</b>"

    if link:
        return f'<a href="https://t.me/{link}">{bold_text}</a>'

    return f'"{bold_text}"' if use_quotes else bold_text


async def get_message(query: CallbackQuery) -> Message:
    """Возвращает объект сообщения или выбрасывает исключение"""
    if isinstance(query.message, Message):
        return query.message

    await query.answer("Произошла ошибка. Попробуйте позже.")

    raise MessageNotAvailableError


async def safe_edit_message(  # noqa: C901 Too complex
    entity: CallbackQuery | Message, *, try_answer: bool = False, **kwargs: Unpack[EditMessageKwargs]
) -> None:
    message: Message | None = None

    if isinstance(entity, CallbackQuery):
        if isinstance(entity.message, Message):
            message = entity.message
        elif isinstance(entity.message, InaccessibleMessage):
            logger.warning("Cannot edit inaccessible message, using try_answer=True")
            try_answer = True

    if isinstance(entity, Message):
        message = entity

    if not message:
        logger.error("Message is not available")
        return

    try:
        await message.edit_text(**kwargs)
    except TelegramBadRequest as bad_request_error:
        if "message is not modified" in bad_request_error.message:
            raise MessageNotModifiedError from bad_request_error
        logger.exception("Failed to edit message with TelegramBadRequest", exc_info=bad_request_error)
        await entity.answer("Произошла ошибка. Попробуйте позже.")
    except Exception as e:
        if try_answer:
            try:
                await message.answer(**kwargs)
            except Exception as answer_error:
                logger.exception("Failed to answer message", exc_info=answer_error)
        else:
            logger.exception("Failed to edit message", exc_info=e)
