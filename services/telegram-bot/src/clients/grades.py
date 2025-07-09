from clients import BaseClient
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from schemas import GradeResponse


__all__ = ["GradeClient"]


class GradeClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/grades")

    async def get_grades(self) -> GradeResponse:
        response = await self.client.get(self.url)
        return GradeResponse.model_validate(response.json())
