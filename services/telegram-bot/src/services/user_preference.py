from common.shared.services import BaseService
from database.models import User, UserPreference
from repositories.user_preference import UserPreferenceRepository


__all__ = ["UserPreferenceService"]


class UserPreferenceService(BaseService[UserPreferenceRepository]):
    async def toggle_preference(self, user: User, category_code: str, item_id: int, item_name: str) -> bool:
        """
        Переключает состояние предпочтения для пользователя.

        Если предпочтение было - удаляет его.
        Если не было - добавляет.

        Возвращает True, если предпочтение было добавлено, False — если удалено.
        """
        existing_preference = await self._repo.get_by_user_and_item(
            user_id=user.id,
            category_code=category_code,
            item_id=item_id,
        )

        if existing_preference:
            await self._repo.delete(existing_preference)
            return False

        new_preference = UserPreference(
            user_id=user.id,
            category_code=category_code,
            item_id=item_id,
            item_name=item_name,
        )
        await self._repo.add(new_preference)
        return True
