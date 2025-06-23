from api.v1 import vacancies
from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()
router.include_router(vacancies.router)
