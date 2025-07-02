from common.environment.config import env_config
from common.logger import get_logger
from common.logger.config import log_config
from fastapi import FastAPI
from schemas import HealthResponse
from seeds import seed_models
import uvicorn
import uvloop


logger = get_logger(__name__)

app = FastAPI(title="Vacancy Processor Service")


@app.get("/health")
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="Healthy")


async def main() -> None:
    await seed_models()

    uvicorn.run(
        "main:app",
        host=env_config.service_internal_host,
        port=env_config.service_internal_port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )


if __name__ == "__main__":
    uvloop.run(main())
