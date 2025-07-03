from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


__all__ = ()


router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer("You started the bot")
