from common.shared.clients.http import http_client
from httpx import URL, AsyncClient


__all__ = ["BaseClient"]


class BaseClient:
    url: URL

    def __init__(self, client: AsyncClient = http_client) -> None:
        self.client = client
        self.configure_client()

    def configure_client(self) -> None:
        """Конфигурирует клиент перед работой"""
