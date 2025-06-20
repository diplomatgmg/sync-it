from common.redis.enums import RedisDbEnum
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["RedisConnectionConfig"]


class RedisConnectionConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)
    db: RedisDbEnum = Field(RedisDbEnum.NOT_SET)

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def dsn(self) -> RedisDsn:
        if self.db == RedisDbEnum.NOT_SET:
            raise ValueError("Redis DB not configured")

        return RedisDsn(f"redis://{self.host}:{self.port}/{self.db}")
