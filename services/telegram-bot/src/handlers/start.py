from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from callbacks.main import MenuActionEnum, MenuCallback
from commands import BotCommandEnum
from database.models import User
from keyboard.inline.main import main_keyboard
from repositories import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from utils.message import make_linked, safe_edit_message

from services import UserService


__all__ = ["router"]


router = Router(name=BotCommandEnum.START)


async def send_welcome_message(target: Message | CallbackQuery, user: User) -> None:
    linked_full_name = make_linked(user.full_name, user.username)

    await safe_edit_message(
        target,
        text=f"Привет, {linked_full_name} 👋",
        reply_markup=main_keyboard(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


@router.message(Command(BotCommandEnum.START))
async def handle_start(message: Message, user: User) -> None:
    await send_welcome_message(message, user)


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.MAIN))
async def handle_main_callback(callback: CallbackQuery, session: AsyncSession) -> None:
    repo = UserRepository(session)
    service = UserService(repo)
    user = await service.get(callback.from_user.id)

    await send_welcome_message(callback, user)
