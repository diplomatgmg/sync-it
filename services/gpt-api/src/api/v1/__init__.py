from api.v1 import completion
from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()
router.include_router(completion.router)
