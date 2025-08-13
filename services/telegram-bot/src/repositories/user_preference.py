from common.shared.repositories import BaseRepository
from database.models import UserPreference
from sqlalchemy import select


__all__ = ["UserPreferenceRepository"]


class UserPreferenceRepository(BaseRepository):
    async def get_by_user_and_item(self, user_id: int, category_code: str, item_id: int) -> UserPreference | None:
        """Находит предпочтение по пользователю, категории и ID опции."""
        stmt = select(UserPreference).where(
            UserPreference.user_id == user_id,
            UserPreference.category_code == category_code,
            UserPreference.item_id == item_id,
        )
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def add(self, user_preference: UserPreference) -> UserPreference:
        """Добавляет новое предпочтение."""
        self._session.add(user_preference)
        await self._session.flush()
        await self._session.refresh(user_preference)

        return user_preference

    async def delete(self, user_preference: UserPreference) -> None:
        """Удаляет существующее предпочтение."""
        await self._session.delete(user_preference)
        await self._session.flush()
