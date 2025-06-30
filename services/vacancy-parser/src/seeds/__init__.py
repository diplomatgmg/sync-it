from seeds.source import seed_sources


__all__ = ["seed_models"]


async def seed_models() -> None:
    """Актуализирует записи константных моделей в базу данных."""
    await seed_sources()
