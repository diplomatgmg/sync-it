from pathlib import Path

from api.v1 import router as v1_router
from common.environment.config import env_config
from common.logger import get_logger
from common.logger.config import log_config
from fastapi import FastAPI
from schemas import HealthResponse
from seeds import seed_models
import uvicorn


logger = get_logger(__name__)

app = FastAPI(title="Vacancy Processor Service")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="Healthy")


def main() -> None:
    service_root_path = Path(__file__).parents[1]
    service_libs_path = Path(__file__).parents[3] / "libs"

    uvicorn.run(
        "main:app",
        host=env_config.service_internal_host,
        port=env_config.service_internal_port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
        reload_dirs=[
            str(service_root_path),
            str(service_libs_path),
        ],
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_models())

    main()
