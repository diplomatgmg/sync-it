from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.logger import get_logger
from httpx import AsyncClient
from schemas import VacancyResponse, VacancySchema


__all__ = ["fetch_new_vacancies"]


logger = get_logger(__name__)


async def fetch_new_vacancies() -> list[VacancySchema]:
    """Возвращает список актуальных вакансий для обработки"""
    url = build_service_url(ServiceEnum.VACANCY_PARSER, "/api/v1/vacancies")

    async with AsyncClient() as client:
        response = await client.get(str(url))
        response.raise_for_status()

    data = VacancyResponse(**response.json())

    return data.vacancies
