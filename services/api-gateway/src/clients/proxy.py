from common.environment.config import env_config
from common.gateway.enums import ServiceEnum
from common.shared.clients import BaseClient
from fastapi import Request, Response
from pydantic import HttpUrl


__all__ = ["proxy_client"]


class _ProxyClient(BaseClient):
    def configure_client(self) -> None:
        self.client.timeout = 60

    async def proxy_request(self, service: ServiceEnum, path: str, request: Request) -> Response:
        """Перенаправляет входящий запрос на указанный сервис."""
        url = HttpUrl.build(
            scheme="http",
            host=service,
            port=env_config.service_internal_port,
            path=path,
        )

        response = await self.client.request(
            method=request.method,
            url=str(url),
            headers=request.headers,
            params=str(request.query_params),  # Без str некорректно формирует list params
            content=await request.body(),
        )

        return Response(
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
        )


proxy_client = _ProxyClient()
