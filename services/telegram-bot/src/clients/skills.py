from async_lru import alru_cache
from clients.schemas import SkillCategoryResponse, SkillCategorySchema, SkillResponse, SkillSchema
from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from common.shared.clients import BaseClient


__all__ = ["skill_category_client", "skill_client"]


class _SkillClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/skills")

    @alru_cache(ttl=60 * 60 * 24)
    async def get_by_category_id(self, category_id: int) -> list[SkillSchema]:
        response = await self.client.get(self.url, params={"category_id": category_id})
        data = response.json()
        model_response = SkillResponse.model_validate(data)

        return model_response.skills


class _SkillCategoryClient(BaseClient):
    url = build_service_url(ServiceEnum.VACANCY_PROCESSOR, "api/v1/skills/categories")

    @alru_cache(ttl=60 * 60 * 24)
    async def get_all(self) -> list[SkillCategorySchema]:
        response = await self.client.get(self.url)
        data = response.json()
        model_response = SkillCategoryResponse.model_validate(data)

        return model_response.skill_categories


skill_client = _SkillClient()
skill_category_client = _SkillCategoryClient()
