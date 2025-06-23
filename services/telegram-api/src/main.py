from api.v1 import router as v1_router
from common.environment.config import env_config
from common.logger import get_logger
from common.logger.config import log_config
from core.config import service_config
from fastapi import FastAPI, HTTPException
import httpx
from schemas import HealthResponse
from utils import validate_health_response
import uvicorn


logger = get_logger(__name__)

app = FastAPI(title="Telegram Parser API Service")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def healthcheck() -> HealthResponse:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://t.me/s/telegram")
            validate_health_response(resp)
        return HealthResponse(status="Healthy")
    except Exception as e:
        logger.exception("Healthcheck failed", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=service_config.host,
        port=service_config.port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )
