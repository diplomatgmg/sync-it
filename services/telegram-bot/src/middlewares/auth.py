from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from schemas.user import UserCreate


if TYPE_CHECKING:
    from services import UserService


__all__ = ["AuthMiddleware"]


class AuthMiddleware(BaseMiddleware):
    """Добавляет пользователя в базу, если он ещё не создан."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        telegram_user = event.from_user
        if telegram_user is None:
            return await handler(event, data)

        user_service: UserService = data["user_service"]

        user = await user_service.get_by_telegram_id(telegram_user.id)
        if not user:
            user_create = UserCreate(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )
            user = await user_service.add_user(user_create)

        data["user"] = user

        return await handler(event, data)
