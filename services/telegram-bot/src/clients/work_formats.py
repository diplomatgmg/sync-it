from async_lru import alru_cache
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.shared.clients import BaseClient
from schemas_bot import WorkFormat, WorkFormatResponse


__all__ = ["work_format_client"]


class _WorkFormatClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/work_formats")

    @alru_cache(ttl=60 * 60 * 24)
    async def get_all(self) -> list[WorkFormat]:
        response = await self.client.get(self.url)
        model_response = WorkFormatResponse.model_validate(response.json())
        return model_response.work_formats


work_format_client = _WorkFormatClient()
