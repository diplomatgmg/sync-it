from common.logger import get_logger
from common.shared.repositories import BaseRepository
from database.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload


__all__ = ["UserRepository"]


logger = get_logger(__name__)


class UserRepository(BaseRepository):
    async def get_by_telegram_id(self, telegram_id: int, *, with_preferences: bool = False) -> User:
        # FIXME: При изменении username, first_name, last_name данные не актуализируются
        stmt = select(User).where(User.telegram_id == telegram_id)

        if with_preferences:
            stmt = stmt.options(selectinload(User.preferences))

        result = await self._session.execute(stmt)

        return result.scalar_one()

    async def add(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)

        return user
