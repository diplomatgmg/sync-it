from api.schemas import HealthResponse
from fastapi import APIRouter


router = APIRouter()


@router.get("")
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="Healthy")
