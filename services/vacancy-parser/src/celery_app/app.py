import asyncio

from celery import Celery  # type: ignore[import-untyped]
from celery_app.beat import beat_schedule
from celery_app.config import celery_config


__all__ = [
    "app",
    "loop",
]


loop = asyncio.new_event_loop()
app = Celery("vacancy-parser", broker=str(celery_config.connection.dsn))

app.conf.beat_schedule = beat_schedule
app.autodiscover_tasks(["tasks"])
