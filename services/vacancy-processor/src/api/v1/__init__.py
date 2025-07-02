from api.v1 import grade, profession, skill
from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()
router.include_router(skill.router)
router.include_router(grade.router)
router.include_router(profession.router)
