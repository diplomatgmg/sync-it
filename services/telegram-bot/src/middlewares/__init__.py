from aiogram import Dispatcher
from common.environment.config import env_config
from common.logger import get_logger
from middlewares.auth import AuthMiddleware
from middlewares.database import DatabaseMiddleware
from middlewares.logging import LoggingMiddleware


__all__ = ["register_middlewares"]


logger = get_logger(__name__)


def register_middlewares(dp: Dispatcher) -> None:
    logger.info("Registering middlewares")

    if env_config.debug:
        dp.update.middleware(LoggingMiddleware())

    dp.update.outer_middleware(DatabaseMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
