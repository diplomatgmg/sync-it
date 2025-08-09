from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.shared.clients import BaseClient
from schemas import Vacancy, VacancyRequest, VacancyResponse


__all__ = ["vacancy_client"]


class _VacancyClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/vacancies")

    async def get_filtered(
        self,
        professions: list[str] | None = None,
        grades: list[str] | None = None,
        work_formats: list[str] | None = None,
        skills: list[str] | None = None,
    ) -> list[Vacancy]:
        params_model = VacancyRequest(professions=professions, grades=grades, work_formats=work_formats, skills=skills)

        response = await self.client.get(
            self.url,
            params=params_model.model_dump(exclude_none=True),
        )
        model_response = VacancyResponse.model_validate(response.json())

        return model_response.vacancies


vacancy_client = _VacancyClient()
