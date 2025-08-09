from typing import cast

from common.logger import get_logger
from fastapi import HTTPException
from g4f.Provider import Chatai  # type: ignore[import-untyped]
from g4f.client import AsyncClient  # type: ignore[import-untyped]


__all__ = ["get_gpt_response"]


logger = get_logger(__name__)


async def get_gpt_response(prompt: str) -> str:
    client = AsyncClient()

    try:
        response = await client.chat.completions.create(
            provider=Chatai,
            messages=[{"role": "user", "content": prompt}],
        )
        return cast("str", response.choices[0].message.content)
    except Exception as e:
        msg = "Failed to get GPT response"
        logger.exception(msg, exc_info=e)
        raise HTTPException(status_code=500, detail=msg) from e
