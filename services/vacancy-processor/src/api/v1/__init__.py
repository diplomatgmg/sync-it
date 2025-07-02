from api.v1 import grade, profession, skill, vacancies, work_format
from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()
router.include_router(vacancies.router)
router.include_router(skill.router)
router.include_router(grade.router)
router.include_router(profession.router)
router.include_router(work_format.router)
