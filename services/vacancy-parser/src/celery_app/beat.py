from datetime import timedelta


__all__ = [
    "beat_schedule",
]

beat_schedule = {
    "load-vacancies-every-hour": {
        "task": "load_vacancies",
        "schedule": timedelta(hours=1),
    }
}
