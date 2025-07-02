from datetime import timedelta

from celery.schedules import schedule  # type: ignore[import-untyped]


__all__ = ["beat_schedule"]

beat_schedule = {
    "parse-vacancies-every-hour": {
        "task": "parse_vacancies",
        "schedule": schedule(run_every=timedelta(hours=1)),
    }
}
