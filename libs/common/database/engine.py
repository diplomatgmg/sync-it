from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from common.database.config import db_config
from common.database.logging import setup_alchemy_logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


__all__ = [
    "get_async_session",
    "provide_async_session",
]


setup_alchemy_logging()


engine = create_async_engine(db_config.url)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def provide_async_session() -> AsyncSession:
    """Обёртка над get_async_session, где не поддерживается контекстный менеджер."""
    async with get_async_session() as session:
        return session
