from aiogram import Dispatcher
from common.logger import get_logger
from middlewares.auth import AuthMiddleware
from middlewares.database import DatabaseMiddleware


__all__ = ["register_middlewares"]


logger = get_logger(__name__)


def register_middlewares(dp: Dispatcher) -> None:
    logger.info("Registering middlewares")

    dp.update.outer_middleware(DatabaseMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
