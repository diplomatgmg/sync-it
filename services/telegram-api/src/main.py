from pathlib import Path

from api.v1 import router as v1_router
from common.environment.config import env_config
from common.logger import get_logger
from common.logger.config import log_config
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from schemas import HealthResponse
from utils import validate_health_response
import uvicorn


logger = get_logger(__name__)

app = FastAPI(title="Telegram Parser API Service")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def healthcheck() -> HealthResponse:
    try:
        async with AsyncClient() as client:
            resp = await client.get("https://t.me/s/telegram")
            validate_health_response(resp)
        return HealthResponse(status="Healthy")
    except Exception as e:
        logger.exception("Healthcheck failed", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e


def main() -> None:
    uvicorn.run(
        "main:app",
        host=env_config.service_internal_host,
        port=env_config.service_internal_port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
        reload_dirs=[str(Path(__file__).parents[3] / "libs")],
    )


if __name__ == "__main__":
    main()
