from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from commands import BotCommandEnum
from schemas.user import UserRead


__all__ = ["router"]


router = Router(name=BotCommandEnum.WHOAMI)


@router.message(Command(BotCommandEnum.WHOAMI))
async def handle_whoami(message: Message, user: UserRead) -> None:
    await message.answer(
        f"Привет, {user.full_name}! @{user.username} 👋\n"
        f"Твой ID в базе: {user.id}\n"
        f"Дата регистрации: {user.created_at.strftime('%d.%m.%Y %H:%M')}"
    )
