from common.logger import get_logger
from core.config import service_config
import httpx
from schemas import CompletionResponse, VacancyResponse
from serializers import VacancySerializer


__all__ = [
    "fetch_gpt_completion",
    "fetch_new_vacancies",
]


logger = get_logger(__name__)


async def fetch_new_vacancies() -> list[VacancySerializer]:
    """Возвращает список актуальных вакансий для обработки"""
    url = f"{service_config.vacancy_parser_url}/api/v1/vacancies"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    data = VacancyResponse(**response.json())

    return data.vacancies


async def fetch_gpt_completion(prompt: str) -> str:
    """Возвращает обработанную промпт через GPT"""
    url = f"{service_config.gpt_api_url}/api/v1/completion"

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json={"prompt": prompt})
        response.raise_for_status()

    data = CompletionResponse(**response.json())

    return data.message
