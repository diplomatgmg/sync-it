from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from email.header import Header
from pathlib import Path
from typing import Annotated

from aiogram.types import Update
from common.environment.config import env_config
from common.logger.config import log_config
from core import service_config
from core.loader import bot, dp
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from setup.lifespan import on_shutdown, on_startup
from starlette import status
import uvicorn


__all__ = ["start_webhook"]


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await on_startup()
    yield
    await on_shutdown()


app = FastAPI(lifespan=lifespan)


async def verify_telegram_secret(  # noqa: RUF029
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
) -> None:
    """Проверяет секретный токен, присланный от Telegram."""
    if service_config.webhook_api_key != x_telegram_bot_api_secret_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret token")


@app.post("/webhook", dependencies=[Depends(verify_telegram_secret)])
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
        secret_token=service_config.webhook_api_key,
    )

    server_config = uvicorn.Config(
        "setup.webhook:app",
        host=env_config.service_internal_host,
        port=env_config.service_internal_port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
        reload_dirs=[str(Path(__file__).parents[4] / "libs")],
    )
    server = uvicorn.Server(server_config)
    await server.serve()
