from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from commands import BotCommandEnum


__all__ = ()


router = Router(name="start")


@router.message(Command(BotCommandEnum.START))
async def handle_start(message: Message) -> None:
    await message.answer("Bot started")
