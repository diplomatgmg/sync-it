from common.logger import get_logger
from core.config import service_config
import httpx
from schemas import CompletionResponse


__all__ = ["fetch_gpt_completion"]


logger = get_logger(__name__)


async def fetch_gpt_completion(prompt: str) -> str:
    """Возвращает обработанную промпт через GPT"""
    url = f"{service_config.gpt_api_url}/api/v1/completion"

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json={"prompt": prompt})
        response.raise_for_status()

    data = CompletionResponse(**response.json())

    return data.message
