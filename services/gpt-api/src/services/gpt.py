import asyncio
from typing import cast

from common.logger import get_logger
from common.shared.decorators.concurency import limit_requests
from fastapi import HTTPException
from g4f.Provider import PollinationsAI  # type: ignore[import-untyped]
from g4f.client import AsyncClient  # type: ignore[import-untyped]
from g4f.typing import Message  # type: ignore[import-untyped]


__all__ = ["get_gpt_response"]


logger = get_logger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 3

client = AsyncClient()


@limit_requests(35)
async def get_gpt_response(prompt: str) -> str:
    message = Message(role="user", content=prompt)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await client.chat.completions.create(
                provider=PollinationsAI,
                messages=[message],
            )
            content = cast("str", response.choices[0].message.content)

            if "502 Bad Gateway" not in content:
                return content

            logger.warning("Got 502, retrying (%s/%s)...", attempt, MAX_RETRIES)
            await asyncio.sleep(RETRY_DELAY)

        except Exception as e:
            logger.exception("Failed to get GPT response on attempt %s", attempt, exc_info=e)
            if attempt == MAX_RETRIES:
                raise HTTPException(status_code=500, detail="Failed to get GPT response") from e
            await asyncio.sleep(RETRY_DELAY)

    raise HTTPException(status_code=500, detail=f"Failed to get GPT response after {MAX_RETRIES} retries")
