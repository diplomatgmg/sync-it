from datetime import timedelta

from celery.schedules import schedule


__all__ = ["beat_schedule"]

beat_schedule = {
    "process-vacancies-5-minutes": {
        "task": "process_vacancies",
        "schedule": schedule(run_every=timedelta(minutes=5)),
    }
}
