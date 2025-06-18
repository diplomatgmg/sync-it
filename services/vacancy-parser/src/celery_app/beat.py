from datetime import timedelta


__all__ = [
    "beat_schedule",
]

beat_schedule = {
    "example-task-every-5-seconds": {
        "task": "example_task",
        "schedule": timedelta(seconds=5),
    },
}
