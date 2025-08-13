from common.logger import get_logger
from common.shared.services.base import BaseUOWService
from database.models import UserPreference
from schemas.user_preference import UserPreferenceCreate
from unitofwork import UnitOfWork


__all__ = ["UserPreferenceService"]


logger = get_logger(__name__)


class UserPreferenceService(BaseUOWService[UnitOfWork]):
    async def toggle_preference(self, user_preference: UserPreferenceCreate) -> bool:
        """
        Переключает состояние предпочтения для пользователя.

        Если предпочтение было - удаляет его.
        Если не было - добавляет.

        Возвращает True, если предпочтение было добавлено, False — если удалено.
        """
        logger.debug(
            "Toggle preference for user id %s, category code: %s, item id: %s",
            user_preference.user_id,
            user_preference.category_code,
            user_preference.item_id,
        )

        existing_preference = await self._uow.user_preferences.get_by_user_and_item(
            user_id=user_preference.user_id,
            category_code=user_preference.category_code,
            item_id=user_preference.item_id,
        )

        if existing_preference:
            await self._uow.user_preferences.delete(existing_preference)
            return False

        new_preference = UserPreference(
            user_id=user_preference.user_id,
            category_code=user_preference.category_code,
            item_id=user_preference.item_id,
            item_name=user_preference.item_name,
        )
        await self._uow.user_preferences.add(new_preference)

        return True
