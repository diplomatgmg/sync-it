from typing import Annotated

from common.environment.config import env_config
from common.gateway.config import gateway_config
from fastapi import Header, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
from starlette.requests import Request


__all__ = ["validate_api_key"]


api_key_header = APIKeyHeader(name="X-API-Key")


async def validate_api_key(request: Request, x_api_key: Annotated[str | None, Header()] = None) -> None:  # noqa: RUF029
    """Проверяет переданный API-ключ."""
    host = f"api-gateway:{gateway_config.port}"
    if request.headers["host"] == host:
        return

    if env_config.debug:
        return

    if x_api_key == gateway_config.api_key:
        return

    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing API Key",
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API Key",
    )
