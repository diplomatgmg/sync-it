from common.shared.clients.http import http_client
from httpx import URL, AsyncClient


__all__ = ["BaseClient"]


class BaseClient:  # noqa: B903 Class could be dataclass or namedtuple
    url: URL

    def __init__(self, client: AsyncClient = http_client) -> None:
        self.client = client
        self.configure_client()

    def configure_client(self) -> None:
        """Конфигурирует клиент перед работой"""
