from common.logger import get_logger
import httpx


__all__ = ["get_newest_vacancies"]


logger = get_logger(__name__)


async def get_newest_vacancies() -> list[str]:
    logger.debug("Getting newest vacancies from vacancy-parser service")

    url = "http://vacancy-parser:8002/api/v1/vacancies"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    return [response.text]
