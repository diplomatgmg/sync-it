from api.v1 import grade, profession, skill, vacancies, work_format
from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()
router.include_router(vacancies.router, prefix="/vacancies")
router.include_router(skill.router, prefix="/skills")
router.include_router(grade.router, prefix="/grades")
router.include_router(profession.router, prefix="/professions")
router.include_router(work_format.router, prefix="/work_formats")
