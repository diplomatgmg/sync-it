from datetime import timedelta


__all__ = [
    "beat_schedule",
]

beat_schedule = {
    "load-telegram-vacancies-every-hour": {
        "task": "load_telegram_vacancies",
        "schedule": timedelta(hours=1),
    }
}
