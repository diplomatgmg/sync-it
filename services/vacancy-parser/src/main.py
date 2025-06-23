from api.v1 import router as v1_router
from common.environment.config import env_config
from common.logger import get_logger
from common.logger.config import log_config
from core.config import parser_config
from fastapi import FastAPI
from schemas import HealthResponse


logger = get_logger(__name__)

app = FastAPI(title="Telegram Parser API Service")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="Healthy")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=parser_config.host,
        port=parser_config.port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )
