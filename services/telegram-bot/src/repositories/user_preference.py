from common.shared.repositories import BaseRepository
from database.models import UserPreference
from sqlalchemy import delete


__all__ = ["UserPreferenceRepository"]


class UserPreferenceRepository(BaseRepository):
    async def add_bulk(self, preferences: list[UserPreference]) -> list[UserPreference]:
        """Добавляет несколько предпочтений за один запрос."""
        self._session.add_all(preferences)
        await self._session.flush()

        return preferences

    async def delete_all_by_user_and_category(self, user_id: int, category_code: str) -> None:
        """Удаляет все предпочтения пользователя по категории."""
        stmt = delete(UserPreference).where(
            UserPreference.user_id == user_id,
            UserPreference.category_code == category_code,
        )
        await self._session.execute(stmt)
        await self._session.flush()
