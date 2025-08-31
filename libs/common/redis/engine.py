from functools import lru_cache
from typing import cast

from common.redis.config import redis_config
from redis import Redis
from redis.asyncio import Redis as AsyncRedis


__all__ = [
    "get_async_redis_cache_client",
    "get_sync_redis_cache_client",
]


@lru_cache
def get_async_redis_cache_client() -> AsyncRedis:
    return cast("AsyncRedis", AsyncRedis.from_url(str(redis_config.cache_dsn)))


@lru_cache
def get_sync_redis_cache_client() -> Redis:
    return Redis.from_url(str(redis_config.cache_dsn))
