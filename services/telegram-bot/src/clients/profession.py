from async_lru import alru_cache
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.shared.clients import BaseClient
from schemas import Profession, ProfessionResponse


__all__ = ["profession_client"]


class _ProfessionClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/professions")

    @alru_cache(ttl=60 * 60 * 24)
    async def get_all(self) -> list[Profession]:
        response = await self.client.get(self.url)
        model_response = ProfessionResponse.model_validate(response.json())
        return model_response.professions


profession_client = _ProfessionClient()
