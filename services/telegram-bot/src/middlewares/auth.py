from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from repositories import UserRepository

from services import UserService


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

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

        session: AsyncSession = data["session"]
        user = event.from_user

        if user is None:
            return await handler(event, data)

        user_repo = UserRepository(session)
        user_service = UserService(user_repo)

        user_model = await user_service.get_or_create(user)
        data["user"] = user_model

        return await handler(event, data)
