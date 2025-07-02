import asyncio

from common.gateway.enums import ServiceEnum
from common.gateway.utils import build_service_url
from httpx import AsyncClient
from schemas import CompletionResponse


__all__ = ["fetch_gpt_completion"]


semaphore = asyncio.Semaphore(15)


async def fetch_gpt_completion(prompt: str) -> str:
    """Возвращает обработанную промпт через GPT"""
    url = build_service_url(ServiceEnum.GPT_API, "/api/v1/completion")

    async with semaphore, AsyncClient(timeout=60) as client:
        response = await client.post(str(url), json={"prompt": prompt})
        response.raise_for_status()

    data = CompletionResponse(**response.json())

    return data.message
