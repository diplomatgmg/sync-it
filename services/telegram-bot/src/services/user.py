from aiogram.types import User as TelegramUser
from common.logger import get_logger
from common.shared.services import BaseService
from database.models import User
from repositories import UserRepository
from sqlalchemy.exc import NoResultFound


__all__ = ["UserService"]

logger = get_logger(__name__)


class UserService(BaseService[UserRepository]):
    async def get(self, telegram_id: int, *, with_preferences: bool = False) -> User:
        return await self._repo.get_by_telegram_id(telegram_id, with_preferences=with_preferences)

    async def get_or_create(self, telegram_user: TelegramUser) -> User:
        """Получает пользователя по telegram_id. Если его нет, создает нового."""
        try:
            return await self.get(telegram_user.id)
        except NoResultFound:
            logger.debug("User with telegram_id %s not found. Creating new user.", telegram_user.id)
            user_model = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )

            return await self._repo.create(user_model)
