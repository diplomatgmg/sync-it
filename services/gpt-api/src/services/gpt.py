import asyncio
from typing import cast

from common.logger import get_logger
from common.shared.decorators.concurency import limit_requests
from g4f.Provider import OIVSCodeSer0501  # type: ignore[import-untyped]
from g4f.client import AsyncClient  # type: ignore[import-untyped]
from g4f.typing import Message  # type: ignore[import-untyped]


__all__ = ["get_gpt_response"]


logger = get_logger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 3

client = AsyncClient()


@limit_requests(35)
async def get_gpt_response(prompt: str) -> str | None:
    message = Message(role="user", content=prompt)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await client.chat.completions.create(
                provider=OIVSCodeSer0501,
                model="gpt-4.1-mini",
                messages=[message],
            )
            content = cast("str", response.choices[0].message.content)

            if "502 Bad Gateway" not in content:
                logger.debug("Received content: %s", content)
                return content

            logger.warning("Got 502, retrying (%s/%s)...", attempt, MAX_RETRIES)
            await asyncio.sleep(RETRY_DELAY**3)

        except Exception as e:
            logger.exception("Failed to get GPT response on attempt %s", attempt, exc_info=e)
            if attempt == MAX_RETRIES:
                return None
            await asyncio.sleep(RETRY_DELAY)

    return None
