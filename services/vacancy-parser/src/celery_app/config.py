from pydantic_settings import BaseSettings, SettingsConfigDict

from libs.redis.config import RedisConnectionConfig
from libs.redis.enums import RedisDbEnum


__all__ = ["celery_config"]


class CeleryConfig(BaseSettings):
    connection: RedisConnectionConfig = RedisConnectionConfig(db=RedisDbEnum.CELERY)

    model_config = SettingsConfigDict(env_prefix="CELERY_")


celery_config = CeleryConfig()
