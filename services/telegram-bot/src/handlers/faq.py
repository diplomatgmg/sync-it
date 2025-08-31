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


async def send_faq_message(message: Message, *, need_reply_markup: bool = True) -> None:
    await message.answer(
        "ℹ️ <b>Что это за бот?</b>\n\n"
        "Этот бот помогает искать релевантные для Вас вакансии, "
        "основываясь на вашем опыте, технологиях и предпочтениях.\n\n"
        "ℹ️ <b>Что делать, если нет вакансий?</b>\n\n"
        "1. Добавьте больше навыков в профиль (желательно 10 и больше).\n"
        "2. Попробуйте снять часть фильтров: грейд, формат работы или профессию.\n"
        "3. Разрешите предпочтения с пометкой <i>«Неизвестно»</i>.\n\n"
        f"❓ Если возникли вопросы или ошибки — напишите в поддержку: @{service_config.support_username}",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard() if need_reply_markup else None,
    )
