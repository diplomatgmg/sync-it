from clients import BaseClient
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from schemas import ProfessionResponse


__all__ = ["ProfessionClient"]


class ProfessionClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/professions")

    async def get_professions(self) -> ProfessionResponse:
        response = await self.client.get(self.url)
        return ProfessionResponse.model_validate(response.json())
