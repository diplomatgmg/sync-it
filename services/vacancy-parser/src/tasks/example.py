from celery_app import app


@app.task(name="example_task")  # type: ignore[misc]
def example_task() -> str:
    return "test"
