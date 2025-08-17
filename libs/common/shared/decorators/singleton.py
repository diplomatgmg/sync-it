from collections.abc import Callable
from datetime import timedelta
from functools import wraps
from typing import ParamSpec, TypeVar

from common.logger import get_logger
from common.redis.engine import sync_redis_cache_client


__all__ = ["singleton"]


logger = get_logger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def singleton(cache_ttl: int | timedelta) -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            lock_name = f"lock:{func.__module__}.{func.__name__}"
            acquired = sync_redis_cache_client.set(lock_name, "locked", nx=True, ex=cache_ttl)

            if not acquired:
                logger.info("Function %s.%s is already running", func.__module__, func.__name__)
                return None

            try:
                return func(*args, **kwargs)
            finally:
                sync_redis_cache_client.delete(lock_name)

        return wrapper

    return decorator
