import asyncio

from celery import Celery
from celery_app.beat import beat_schedule
from common.redis.config import redis_config
from common.sentry.initialize import init_sentry


__all__ = ["app"]


init_sentry()

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)

app = Celery(
    "vacancy-processor",
    broker=str(redis_config.celery_broker_dsn),
    backend=str(redis_config.celery_result_dsn),
)
app.conf.task_default_queue = "processor_queue"
app.conf.beat_schedule = beat_schedule
app.autodiscover_tasks(["tasks"])
