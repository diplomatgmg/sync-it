from typing import NotRequired, TypedDict, Unpack

from aiogram.client.default import Default
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
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


async def get_message(query: CallbackQuery | Message) -> Message:
    """Возвращает объект сообщения или выбрасывает исключение"""
    if isinstance(query, Message):
        return query
    if isinstance(query.message, Message):
        return query.message

    await query.answer("Произошла ошибка. Попробуйте позже.")

    raise MessageNotAvailableError


async def safe_edit_message(
    entity: CallbackQuery | Message,
    **kwargs: Unpack[EditMessageKwargs],
) -> None:
    """
    Безопасно редактирует сообщение.
    Если редактирование невозможно - отправляет новое.
    """
    message = await get_message(entity)

    try:
        await message.edit_text(**kwargs)
    except Exception as err:
        if isinstance(err, TelegramBadRequest) and "message is not modified" in err.message:
            raise MessageNotModifiedError from err

        try:
            await message.answer(**kwargs)
        except Exception as answer_err:
            logger.exception(
                "Failed to edit message and failed to answer as a fallback",
                exc_info=answer_err,
            )
