from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from commands import BotCommandEnum
from core import service_config


__all__ = ()


router = Router(name=BotCommandEnum.SUPPORT)


@router.message(Command("support"))
async def handle_support(message: Message) -> None:
    await message.reply(f"Вопросы, предложения, обратная связь - @{service_config.support_username}")
