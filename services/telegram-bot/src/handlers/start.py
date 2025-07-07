from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from commands import BotCommandEnum
from database.models import User
from keyboard.inline.main import main_keyboard
from utils.message import make_linked


__all__ = ["router"]


router = Router(name=BotCommandEnum.START)


@router.message(Command(BotCommandEnum.START))
async def handle_start(message: Message, user: User) -> None:
    linked_full_name = make_linked(user.full_name, user.username)

    await message.answer(
        f"Привет, {linked_full_name} 👋",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=main_keyboard(),
    )
