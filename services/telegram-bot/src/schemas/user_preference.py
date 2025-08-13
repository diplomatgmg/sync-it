from database.models.enums import PreferenceCategoryCodeEnum
from pydantic import BaseModel, ConfigDict


__all__ = [
    "UserPreferenceCreate",
    "UserPreferenceRead",
]


class UserPreferenceBase(BaseModel):
    user_id: int
    category_code: PreferenceCategoryCodeEnum
    item_id: int
    item_name: str


class UserPreferenceCreate(UserPreferenceBase):
    pass


class UserPreferenceRead(UserPreferenceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
