from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from commands import BotCommandEnum
from core import service_config
from keyboard.inline.main import main_menu_keyboard


__all__ = ["router"]


router = Router(name=BotCommandEnum.FAQ)


@router.message(Command(BotCommandEnum.FAQ))
async def handle_faq_command(message: Message) -> None:
    await send_faq_message(message)


async def send_faq_message(message: Message) -> None:
    await message.answer(
        "ℹ️ <b>Что это за бот?</b>\n\n"
        "Этот бот помогает искать релевантные для Вас вакансии, "
        "основываясь на вашем опыте, технологиях и предпочтениях.\n\n"
        f"❓ Если возникли вопросы или ошибки — напишите в поддержку: @{service_config.support_username}",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard(),
    )
