from api.v1 import channel_messages
from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()
router.include_router(channel_messages.router)
