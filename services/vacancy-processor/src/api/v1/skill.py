from typing import Annotated

from api.depedencies import get_skill_service
from api.v1.schemas import SkillListResponse
from clients import gpt_client
from fastapi import APIRouter, Depends
from schemas.skill import SkillRead
from utils.extractor import VacancyExtractor
from utils.prompter import make_resume_prompt

from services import SkillService


__all__ = ["router"]


router = APIRouter()


@router.get("")
async def get_skills(service: Annotated[SkillService, Depends(get_skill_service)]) -> SkillListResponse:
    """Возвращает актуальные скиллы."""
    skills = await service.get_skills()

    return SkillListResponse(skills=[SkillRead.model_validate(s) for s in skills])


@router.post("/extract")
async def extract_skills(
    text: str,
    service: Annotated[SkillService, Depends(get_skill_service)],
) -> SkillListResponse:
    prompt = make_resume_prompt(text)
    completion = await gpt_client.get_completion(prompt)
    extractor = VacancyExtractor()
    skill_enums = extractor.extract_skills(completion)
    skills = await service.get_skills_by_enums(skill_enums)

    return SkillListResponse(skills=skills)
