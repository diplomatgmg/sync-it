from api.v1 import skill
from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()
router.include_router(skill.router)
