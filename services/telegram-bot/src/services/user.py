from aiogram.types import User as TelegramUser
from common.shared.services import BaseService
from database.models import User
from repositories import UserRepository


__all__ = ["UserService"]


class UserService(BaseService[UserRepository]):
    async def get_or_create(self, telegram_user: TelegramUser) -> User:
        """Получает пользователя по telegram_id. Если его нет, создает нового."""
        db_user = await self._repo.get_by_telegram_id(telegram_user.id)
        if db_user:
            return db_user

        user_model = User(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
        )

        return await self._repo.create(user_model)
