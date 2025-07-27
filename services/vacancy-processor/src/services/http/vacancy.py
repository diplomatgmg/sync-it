from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.logger import get_logger
from httpx import AsyncClient
from schemas import ParsedVacancyDeleteResponse, ParsedVacancyResponse, ParsedVacancySchema


__all__ = [
    "fetch_new_vacancies",
    "send_delete_request_vacancy",
]


logger = get_logger(__name__)


# FIXME: вынести в клиенты


async def fetch_new_vacancies() -> list[ParsedVacancySchema]:
    """Возвращает список актуальных вакансий для обработки"""
    url = build_service_url(ServiceEnum.VACANCY_PARSER, "/api/v1/vacancies")

    async with AsyncClient() as client:
        response = await client.get(str(url))
        response.raise_for_status()

    data = ParsedVacancyResponse(**response.json())

    return data.vacancies


async def send_delete_request_vacancy(vacancy: ParsedVacancySchema) -> None:
    logger.debug("Marking vacancy as deleted: %s, hash: %s", vacancy.link, vacancy.hash)

    url = build_service_url(ServiceEnum.VACANCY_PARSER, f"/api/v1/vacancies/{vacancy.hash}")

    async with AsyncClient() as client:
        response = await client.delete(str(url))
        response.raise_for_status()

    data = ParsedVacancyDeleteResponse(**response.json())

    if not data.is_deleted:
        logger.error("Failed to mark vacancy as deleted: %s", vacancy.link)
        return
