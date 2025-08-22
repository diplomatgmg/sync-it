import asyncio

from celery import Celery
from common.redis.config import redis_config
from common.sentry.initialize import init_sentry


__all__ = ["app"]


init_sentry()

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)

app = Celery(
    "telegram-bot",
    broker=str(redis_config.celery_broker_dsn),
    backend=str(redis_config.celery_result_dsn),
)
app.conf.task_default_queue = "telegram_bot_queue"
app.autodiscover_tasks(["tasks"])
