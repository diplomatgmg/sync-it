from clients import BaseClient
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from schemas import Profession, ProfessionResponse


__all__ = ["ProfessionClient"]


class ProfessionClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/professions")

    async def get_all(self) -> list[Profession]:
        response = await self.client.get(self.url)
        model_response = ProfessionResponse.model_validate(response.json())
        return model_response.professions
