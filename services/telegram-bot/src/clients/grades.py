from async_lru import alru_cache
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.shared.clients import BaseClient
from schemas_bot import Grade, GradeResponse


__all__ = ["grade_client"]


class _GradeClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/grades")

    @alru_cache(ttl=60 * 60 * 24)
    async def get_all(self) -> list[Grade]:
        response = await self.client.get(self.url)
        model_response = GradeResponse.model_validate(response.json())
        return model_response.grades


grade_client = _GradeClient()
