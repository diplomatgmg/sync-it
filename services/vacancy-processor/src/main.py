from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from api import router as health_router
from api.v1 import router as v1_router
from common.environment.config import env_config
from common.logger import get_logger
from common.logger.config import log_config
from fastapi import FastAPI
from seeds import seed_models
import uvicorn


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_fast_api: FastAPI) -> AsyncGenerator[None]:
    await seed_models()
    yield


app = FastAPI(title="Vacancy Processor Service", lifespan=lifespan)
app.include_router(health_router)
app.include_router(v1_router, prefix="/api/v1")


def main() -> None:
    uvicorn.run(
        "main:app",
        host=env_config.service_internal_host,
        port=env_config.service_internal_port,
        log_level=log_config.level.lower(),
    )


if __name__ == "__main__":
    main()
