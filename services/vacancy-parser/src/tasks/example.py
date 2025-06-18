from celery_app import app


@app.task  # type: ignore[misc]
def example_task() -> str:
    return "test"
