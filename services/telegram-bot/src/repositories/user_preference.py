from database.models import UserPreference
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["UserPreferenceRepository"]


class UserPreferenceRepository:
    def __init__(self, session: AsyncSession) -> None:
        # FIXME: лучше везде использовать self._session. Атрибут только для внутреннего использования
        #  Можно будет создать базовый класс BaseRepository с одинаковым init для всех репозиториев
        self.session = session

    async def get_by_user_and_item(self, user_id: int, category_code: str, item_id: int) -> UserPreference:
        """Находит предпочтение по пользователю, категории и ID опции."""
        stmt = select(UserPreference).where(
            and_(
                UserPreference.user_id == user_id,
                UserPreference.category_code == category_code,
                UserPreference.item_id == item_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def add(self, user_preference: UserPreference) -> None:
        """Добавляет новое предпочтение."""
        self.session.add(user_preference)
        await self.session.flush()

    async def delete(self, user_preference: UserPreference) -> None:
        """Удаляет существующее предпочтение."""
        await self.session.delete(user_preference)
        await self.session.flush()
