from aiogram import Bot, Dispatcher
from core import service_config


__all__ = [
    "bot",
    "dp",
]


bot = Bot(token=service_config.token)
dp = Dispatcher()
