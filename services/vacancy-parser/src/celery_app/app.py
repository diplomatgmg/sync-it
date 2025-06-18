from celery import Celery  # type: ignore[import-untyped]
from celery_app.config import celery_config


__all__ = [
    "app",
]


app = Celery("vacancy-parser", broker=str(celery_config.connection.dsn))
