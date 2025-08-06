from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.logger import get_logger
from common.shared.clients import BaseClient
from schemas import ParsedVacancyDeleteResponse, ParsedVacancyResponse, ParsedVacancySchema


__all__ = ["vacancy_client"]


logger = get_logger(__name__)


class _VacancyClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PARSER, "/api/v1/vacancies")

    async def fetch(self) -> list[ParsedVacancySchema]:
        response = await self.client.get(self.url)
        response.raise_for_status()

        data = ParsedVacancyResponse(**response.json())

        return data.vacancies

    async def delete(self, vacancy: ParsedVacancySchema) -> bool:
        detail_vacancy_url = f"{self.url}/{vacancy.hash}"

        response = await self.client.delete(detail_vacancy_url)
        response.raise_for_status()

        model_response = ParsedVacancyDeleteResponse(**response.json())
        if not model_response.is_deleted:
            logger.error("Failed to mark vacancy as deleted: %s", vacancy.link)
            return False

        return True


vacancy_client = _VacancyClient()
