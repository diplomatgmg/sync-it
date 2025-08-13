from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.shared.clients import BaseClient
from schemas_bot import (
    VacancyCursorPaginationRequest,
    VacancyCursorPaginationResponse,
    VacancyCursorPaginationSchema,
)


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
    ) -> VacancyCursorPaginationSchema:
        params_model = VacancyCursorPaginationRequest(
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

        model_response = VacancyCursorPaginationResponse.model_validate(response.json())

        return model_response.result


vacancy_client = _VacancyClient()
