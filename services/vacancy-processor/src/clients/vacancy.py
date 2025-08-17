from clients.schemas import VacancyDeleteResponse, VacancyResponse, VacancySchema
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.logger import get_logger
from common.shared.clients import BaseClient


__all__ = ["vacancy_client"]


logger = get_logger(__name__)


class _VacancyClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PARSER, "/api/v1/vacancies")

    async def get_vacancies(self) -> list[VacancySchema]:
        response = await self.client.get(self.url)
        response.raise_for_status()

        data = VacancyResponse(**response.json())

        return data.vacancies

    async def delete(self, vacancy: VacancySchema) -> bool:
        detail_vacancy_url = f"{self.url}/{vacancy.hash}"

        response = await self.client.delete(detail_vacancy_url)
        response.raise_for_status()

        response_data = VacancyDeleteResponse(**response.json())
        if not response_data.is_deleted:
            logger.error("Failed to mark vacancy as deleted: %s", vacancy.link)
            return False

        return True


vacancy_client = _VacancyClient()
