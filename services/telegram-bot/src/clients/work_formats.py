from clients import BaseClient
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from schemas import WorkFormat, WorkFormatResponse


__all__ = ["WorkFormatClient"]


class WorkFormatClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/work_formats")

    async def get_all(self) -> list[WorkFormat]:
        response = await self.client.get(self.url)
        model_response = WorkFormatResponse.model_validate(response.json())
        return model_response.work_formats
