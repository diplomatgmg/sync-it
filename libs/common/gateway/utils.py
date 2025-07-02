from common.gateway.config import gateway_config
from common.gateway.enums import ServiceEnum
from pydantic import HttpUrl


__all__ = ["build_service_url"]


def build_service_url(service: ServiceEnum, path: str) -> HttpUrl:
    path = path.strip("/")

    return HttpUrl.build(
        scheme="http",
        host="api-gateway",
        port=gateway_config.port,
        path=f"{service}/{path}",
    )
