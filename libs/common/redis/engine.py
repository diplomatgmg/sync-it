from functools import lru_cache

from common.redis.config import redis_config
from redis import Redis


__all__ = ["sync_redis_cache_client"]


@lru_cache
def get_sync_redis_cache_client() -> Redis:
    return Redis.from_url(str(redis_config.cache_dsn))


sync_redis_cache_client = get_sync_redis_cache_client()
