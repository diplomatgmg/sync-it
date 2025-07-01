from common.environment.config import env_config
from common.gateway.enums import ServiceEnum
from common.logger import get_logger
from common.logger.config import log_config
from core.config import service_config
from fastapi import FastAPI, HTTPException, Request, Response
from httpx import AsyncClient
from schemas import HealthResponse
import uvicorn


logger = get_logger(__name__)

app = FastAPI(title="API Gateway Service")


# FIXME: secret_key depends.
@app.api_route("/{service}/{path:path}")
async def gateway_proxy(service: ServiceEnum, path: str, request: Request) -> Response:
    logger.debug("Proxy request to service: %s, path: %s", service, path)

    if service not in ServiceEnum:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"http://{service}:{env_config.service_internal_port}/{path}"
    methods_with_body = {"POST", "PUT", "PATCH"}

    async with AsyncClient() as client:
        json = await request.json() if request.method in methods_with_body else None

        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            params=request.query_params,
            json=json,
            timeout=30,
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
        host=service_config.host,
        port=service_config.port,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )


if __name__ == "__main__":
    main()
