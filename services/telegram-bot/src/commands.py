from aiogram.types import BotCommand
from utils.enums import CommandEnum


__all__ = [
    "BotCommandEnum",
    "get_bot_commands",
]


class BotCommandEnum(CommandEnum):
    START = "start", "Запустить бота"
    WHOAMI = "whoami", "Информация о пользователе"


def get_bot_commands() -> list[BotCommand]:
    return [BotCommand(command=cmd, description=cmd.description) for cmd in BotCommandEnum]
