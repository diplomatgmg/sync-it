from clients import grade_client, profession_client, work_format_client
from clients.protocols import SupportsGetAll
from database.models.enums import PreferencesCategoryCodeEnum


__all__ = [
    "ClientType",
    "get_client",
]

type ClientType = SupportsGetAll

CLIENT_MAP: dict[PreferencesCategoryCodeEnum, ClientType] = {
    PreferencesCategoryCodeEnum.GRADE: grade_client,
    PreferencesCategoryCodeEnum.WORK_FORMAT: work_format_client,
    PreferencesCategoryCodeEnum.PROFESSION: profession_client,
}


def get_client(category: PreferencesCategoryCodeEnum) -> ClientType:
    return CLIENT_MAP[category]
