from collections.abc import Iterable

from common.logger import get_logger
from common.shared.services import BaseUOWService
from database.models import UserPreference
from database.models.enums import PreferenceCategoryCodeEnum
from schemas.user_preference import UserPreferenceCreate
from unitofwork import UnitOfWork


__all__ = ["UserPreferenceService"]


logger = get_logger(__name__)


class UserPreferenceService(BaseUOWService[UnitOfWork]):
    async def replace_user_preferences(
        self,
        user_id: int,
        category_code: PreferenceCategoryCodeEnum,
        preferences: Iterable[UserPreferenceCreate],
    ) -> list[UserPreference]:
        """Полностью заменяет предпочтения пользователя по категории."""
        await self._uow.user_preferences.delete_all_by_user_and_category(user_id, category_code)

        new_preferences = [
            UserPreference(
                user_id=pref.user_id,
                category_code=pref.category_code,
                item_id=pref.item_id,
                item_name=pref.item_name,
            )
            for pref in preferences
        ]

        return await self._uow.user_preferences.add_bulk(new_preferences)
