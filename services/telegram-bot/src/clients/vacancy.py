from clients.schemas import (
    VacancyWithNeighborsRequest,
    VacancyWithNeighborsResponse,
    VacancyWithNeighborsSchema,
)
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.shared.clients import BaseClient


__all__ = ["vacancy_client"]


class _VacancyClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/vacancies")

    async def get_by_id_with_cursor_pagination(
        self,
        vacancy_id: int,
        professions: list[str] | None = None,
        grades: list[str] | None = None,
        work_formats: list[str] | None = None,
        skills: list[str] | None = None,
    ) -> VacancyWithNeighborsSchema:
        params_model = VacancyWithNeighborsRequest(
            professions=professions,
            grades=grades,
            work_formats=work_formats,
            skills=skills,
        )
        url = f"{self.url}/{vacancy_id}"
        response = await self.client.get(
            url,
            params=params_model.model_dump(exclude_none=True),
        )
        data = response.json()
        model_response = VacancyWithNeighborsResponse.model_validate(data)

        return model_response.result


vacancy_client = _VacancyClient()
