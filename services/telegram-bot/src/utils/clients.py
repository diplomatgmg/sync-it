from clients import grade_client, profession_client, work_format_client
from clients.protocols import SupportsGetAll
from database.models.enums import PreferenceCategoryCodeEnum


__all__ = [
    "ClientType",
    "get_client",
]

type ClientType = SupportsGetAll

CLIENT_MAP: dict[PreferenceCategoryCodeEnum, ClientType] = {
    PreferenceCategoryCodeEnum.GRADE: grade_client,
    PreferenceCategoryCodeEnum.WORK_FORMAT: work_format_client,
    PreferenceCategoryCodeEnum.PROFESSION: profession_client,
}


def get_client(category: PreferenceCategoryCodeEnum) -> ClientType:
    return CLIENT_MAP[category]
