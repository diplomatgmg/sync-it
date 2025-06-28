from seeds.profession import seed_professions
from seeds.work_format import seed_work_formats


async def seed_models() -> None:
    """Актуализирует записи константных моделей в базу данных."""
    await seed_work_formats()
    await seed_professions()
