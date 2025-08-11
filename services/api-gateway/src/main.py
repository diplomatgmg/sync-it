from common.environment.config import env_config
from common.gateway.config import gateway_config
from common.gateway.enums import ServiceEnum
from common.logger import get_logger
from common.logger.config import log_config
from dependencies import validate_api_key
from fastapi import Depends, FastAPI, Request, Response
from httpx import AsyncClient
from pydantic import HttpUrl
from schemas import HealthResponse
import uvicorn


logger = get_logger(__name__)


app = FastAPI(title="API Gateway Service")


@app.api_route(
    "/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    dependencies=[Depends(validate_api_key)],
)
async def gateway_proxy(service: ServiceEnum, path: str, request: Request) -> Response:
    logger.debug("Proxy request to service: %s, path: %s", service, path)

    url = HttpUrl.build(
        scheme="http",
        host=service,
        port=env_config.service_internal_port,
        path=path,
    )

    async with AsyncClient(timeout=60) as client:
        methods_with_body = {"POST", "PUT", "PATCH"}
        json = await request.json() if request.method in methods_with_body else None

        response = await client.request(
            method=request.method,
            url=str(url),
            headers=request.headers,
            params=request.query_params,
            json=json,
        )

    return Response(
        status_code=response.status_code,
        headers=response.headers,
        content=response.content,
    )


@app.get("/health")
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="Healthy")


def main() -> None:
    uvicorn.run(
        "main:app",
        host=gateway_config.host,
        port=gateway_config.port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )


if __name__ == "__main__":
    main()
