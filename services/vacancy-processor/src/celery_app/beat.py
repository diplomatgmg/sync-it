from datetime import timedelta

from celery.schedules import schedule  # type: ignore[import-untyped]


__all__ = ["beat_schedule"]

beat_schedule = {
    "process-vacancies-30-minutes": {
        "task": "process_vacancies",
        "schedule": schedule(run_every=timedelta(minutes=30)),
    }
}
