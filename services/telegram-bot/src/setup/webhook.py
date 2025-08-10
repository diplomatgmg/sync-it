from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from aiogram.types import Update
from common.environment.config import env_config
from common.logger.config import log_config
from core import service_config
from core.loader import bot, dp
from fastapi import FastAPI
from pydantic import BaseModel
from setup.lifespan import on_shutdown, on_startup
import uvicorn


__all__ = ["start_webhook"]


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await on_startup()
    yield
    await on_shutdown()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def bot_webhook(update: Update) -> None:
    await dp.feed_webhook_update(bot=bot, update=update)


class HealthResponse(BaseModel):
    status: str


@app.get("/health")
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="Healthy")


async def start_webhook() -> None:
    await bot.set_webhook(
        url=str(service_config.webhook_url),
        drop_pending_updates=True,
    )

    uvicorn.run(
        "setup.webhook:app",
        host=env_config.service_internal_host,
        port=env_config.service_internal_port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )
