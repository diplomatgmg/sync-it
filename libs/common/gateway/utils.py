from common.environment.config import env_config
from common.gateway.enums import ServiceEnum
from pydantic import HttpUrl


__all__ = ["build_service_url"]


def build_service_url(service: ServiceEnum, path: str) -> HttpUrl:
    path = path.strip("/")

    return HttpUrl.build(
        scheme="http",
        host=service,
        port=env_config.service_internal_port,
        path=path,
    )
