from typing import Self

from pydantic import Field, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["redis_config"]


class RedisConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)

    cache_db: int
    celery_broker_db: int
    celery_result_db: int

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def cache_dsn(self) -> RedisDsn:
        return self._dsn(db=self.cache_db)

    @property
    def celery_broker_dsn(self) -> RedisDsn:
        return self._dsn(db=self.celery_broker_db)

    @property
    def celery_result_dsn(self) -> RedisDsn:
        return self._dsn(db=self.celery_result_db)

    @model_validator(mode="after")
    def check_unique_dbs(self) -> Self:
        """Проверяет, что все БД уникальны."""
        db_fields = list(filter(lambda x: x.endswith("_db"), self.model_fields_set))
        dbs = {getattr(self, x) for x in db_fields}

        if len(dbs) != len(db_fields):
            raise ValueError("Databases must be unique")

        return self

    def _dsn(self, db: int) -> RedisDsn:
        return RedisDsn(f"redis://{self.host}:{self.port}/{db}")


redis_config = RedisConfig()
