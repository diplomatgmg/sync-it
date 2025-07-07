from typing import NotRequired, TypedDict, Unpack

from aiogram.client.default import Default
from aiogram.types import CallbackQuery, InaccessibleMessage, InlineKeyboardMarkup, Message
from exceptions import MessageNotAvailableError


__all__ = [
    "get_message",
    "make_linked",
    "safe_edit_message",
]


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


async def safe_edit_message(query: CallbackQuery, **kwargs: Unpack[EditMessageKwargs]) -> None:
    if isinstance(query.message, Message):
        await query.message.edit_text(**kwargs)
        return

    if isinstance(query.message, InaccessibleMessage):
        await query.message.answer(**kwargs)
        return

    await query.answer("Произошла ошибка. Попробуйте позже.")
