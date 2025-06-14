from typing import cast

from g4f.Provider import Blackbox  # type: ignore[import-untyped]
from g4f.client import AsyncClient  # type: ignore[import-untyped]


__all__ = ["get_gpt_response"]


async def get_gpt_response(prompt: str) -> str:
    client = AsyncClient()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        provider=Blackbox,
        messages=[{"role": "user", "content": prompt}],
    )
    return cast("str", response.choices[0].message.content)
