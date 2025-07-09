from clients import BaseClient
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from schemas import WorkFormatResponse


__all__ = ["WorkFormatClient"]


class WorkFormatClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/work_formats")

    async def get_work_formats(self) -> WorkFormatResponse:
        response = await self.client.get(self.url)
        return WorkFormatResponse.model_validate(response.json())
