from clients import proxy_client
from common.gateway.config import gateway_config
from common.gateway.enums import ServiceEnum
from common.logger import get_logger
from common.logger.config import log_config
from common.sentry.enums import IntegrationImportsEnum
from common.sentry.initialize import init_sentry
from dependencies import validate_api_key
from fastapi import Depends, FastAPI, Request, Response
from schemas import HealthResponse
import uvicorn


logger = get_logger(__name__)


app = FastAPI(title="API Gateway Service")


@app.get("/{service}/{path:path}", dependencies=[Depends(validate_api_key)])
async def get_gateway_proxy(service: ServiceEnum, path: str, request: Request) -> Response:
    return await proxy_client.proxy_request(service, path, request)


@app.post("/{service}/{path:path}", dependencies=[Depends(validate_api_key)])
async def post_gateway_proxy(service: ServiceEnum, path: str, request: Request) -> Response:
    return await proxy_client.proxy_request(service, path, request)


@app.delete("/{service}/{path:path}", dependencies=[Depends(validate_api_key)])
async def delete_gateway_proxy(service: ServiceEnum, path: str, request: Request) -> Response:
    return await proxy_client.proxy_request(service, path, request)


@app.get("/health")
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="Healthy")


def main() -> None:
    init_sentry(
        [
            IntegrationImportsEnum.FASTAPI,
            IntegrationImportsEnum.HTTPX,
            IntegrationImportsEnum.LOGGING,
        ]
    )

    uvicorn.run(
        "main:app",
        host=gateway_config.host,
        port=gateway_config.port,
        log_level=log_config.level.lower(),
    )


if __name__ == "__main__":
    main()
