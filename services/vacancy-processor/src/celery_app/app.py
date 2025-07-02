import asyncio

from celery import Celery  # type: ignore[import-untyped]
from celery_app.beat import beat_schedule
from common.redis.config import redis_config


__all__ = [
    "app",
    "loop",
]


loop = asyncio.new_event_loop()
app = Celery(
    "vacancy-processor",
    broker=str(redis_config.celery_broker_dsn),
    backend=str(redis_config.celery_result_dsn),
)

app.conf.beat_schedule = beat_schedule
app.autodiscover_tasks(["tasks"])
