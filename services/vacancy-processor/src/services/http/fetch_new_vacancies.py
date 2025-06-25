from common.logger import get_logger
from core.config import service_config
import httpx
from schemas import VacancyResponse
from serializers import VacancySerializer


__all__ = ["fetch_new_vacancies"]


logger = get_logger(__name__)


async def fetch_new_vacancies() -> list[VacancySerializer]:
    """Возвращает список актуальных вакансий для обработки"""
    url = f"{service_config.vacancy_parser_url}/api/v1/vacancies"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    data = VacancyResponse(**response.json())

    return data.vacancies
