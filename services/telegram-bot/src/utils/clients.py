from clients import GradeClient, ProfessionClient, WorkFormatClient
from database.models.enums import PreferenceCategoryCodeEnum


__all__ = [
    "ClientType",
    "get_client",
]

type ClientType = type[GradeClient | WorkFormatClient | ProfessionClient]

CLIENT_MAP: dict[PreferenceCategoryCodeEnum, ClientType] = {
    PreferenceCategoryCodeEnum.GRADE: GradeClient,
    PreferenceCategoryCodeEnum.WORK_FORMAT: WorkFormatClient,
    PreferenceCategoryCodeEnum.PROFESSION: ProfessionClient,
}


def get_client(category: PreferenceCategoryCodeEnum) -> ClientType:
    return CLIENT_MAP[category]
