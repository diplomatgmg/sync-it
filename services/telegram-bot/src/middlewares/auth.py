from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from database.models import User
from database.services import UserService


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

        user_service = UserService(session)
        user_model = await user_service.get_user(user.id)

        if user_model is None:
            user_model = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            await user_service.add_user(user_model)

        data["user"] = user_model

        return await handler(event, data)
