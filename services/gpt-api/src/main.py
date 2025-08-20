from api.v1 import router as v1_router
from common.environment.config import env_config
from common.logger import get_logger
from common.logger.config import log_config
from common.sentry.initialize import init_sentry
from fastapi import FastAPI, HTTPException
from schemas import HealthResponse
from services.gpt import get_gpt_response
from utils import validate_health_response
import uvicorn


logger = get_logger(__name__)

app = FastAPI(title="GPT API Service")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def healthcheck() -> HealthResponse:
    try:
        response_text = await get_gpt_response('Say "Healthy"')
        validate_health_response(response_text)
        return HealthResponse(status=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def main() -> None:
    init_sentry()

    uvicorn.run(
        "main:app",
        host=env_config.service_internal_host,
        port=env_config.service_internal_port,
        log_level=log_config.level.lower(),
    )


if __name__ == "__main__":
    main()
