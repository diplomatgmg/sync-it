from database.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["UserService"]


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user(self, telegram_id: int) -> User | None:
        # FIXME: При изменении username, first_name, last_name данные не актуализируются
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user
