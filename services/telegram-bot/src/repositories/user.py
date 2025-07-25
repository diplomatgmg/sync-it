from common.shared.repositories import BaseRepository
from database.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload


__all__ = ["UserRepository"]


class UserRepository(BaseRepository):
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        # FIXME: При изменении username, first_name, last_name данные не актуализируются
        stmt = select(User).where(User.telegram_id == telegram_id).options(selectinload(User.preferences))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
