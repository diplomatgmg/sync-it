from enum import IntEnum


__all__ = ["RedisDbEnum"]


class RedisDbEnum(IntEnum):
    NOT_SET = -1
    CELERY = 1
