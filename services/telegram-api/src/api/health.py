from api.schemas import HealthResponse
from clients import telegram_client
from common.logger import get_logger
from fastapi import APIRouter, HTTPException


__all__ = ["router"]

router = APIRouter()


logger = get_logger(__name__)


@router.get("")
async def healthcheck() -> HealthResponse:
    try:
        await telegram_client.ping()

        return HealthResponse(status="Healthy")
    except Exception as e:
        logger.exception("Healthcheck failed", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e
