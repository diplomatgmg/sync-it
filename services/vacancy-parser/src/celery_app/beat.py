from datetime import timedelta

from celery.schedules import schedule  # type: ignore[import-untyped]


__all__ = ["beat_schedule"]

beat_schedule = {
    "parse-vacancies-every-10-minutes": {
        "task": "parse_vacancies",
        "schedule": schedule(run_every=timedelta(minutes=1)),
    }
}
