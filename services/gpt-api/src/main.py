from core.config import api_config
from fastapi import FastAPI, HTTPException
from schemas import HealthResponse, PromptRequest, PromptResponse
from service import get_gpt_response
from utils import validate_health_response
import uvicorn

from libs.environment.config import env_config
from libs.logger import get_logger
from libs.logger.config import log_config


logger = get_logger(__name__)

app = FastAPI(title="GPT API Service")


@app.post("/prompt")
async def prompt_gpt(request: PromptRequest) -> PromptResponse:
    try:
        response_text = await get_gpt_response(request.prompt)
        return PromptResponse(response=response_text)
    except Exception as e:
        logger.exception("Failed to get GPT response", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def healthcheck() -> HealthResponse:
    try:
        response_text = await get_gpt_response('Say "Healthy"')
        validate_health_response(response_text)
        return HealthResponse(status=response_text)
    except Exception as e:
        logger.exception("Healthcheck failed", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e


def main() -> None:
    uvicorn.run(
        "main:app",
        host=api_config.host,
        port=api_config.port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )


if __name__ == "__main__":
    main()
