from enum import StrEnum
import importlib
import logging
from typing import TYPE_CHECKING

from sentry_sdk.integrations import Integration


if TYPE_CHECKING:
    from sentry_sdk.integrations.logging import LoggingIntegration

__all__ = [
    "IntegrationImportsEnum",
    "ProfileLifecycleEnum",
]


class ProfileLifecycleEnum(StrEnum):
    MANUAL = "manual"
    TRACE = "trace"


class IntegrationImportsEnum(StrEnum):
    CELERY = "sentry_sdk.integrations.celery.CeleryIntegration"
    FASTAPI = "sentry_sdk.integrations.fastapi.FastApiIntegration"
    HTTPX = "sentry_sdk.integrations.httpx.HttpxIntegration"
    LOGGING = "sentry_sdk.integrations.logging.LoggingIntegration"
    REDIS = "sentry_sdk.integrations.redis.RedisIntegration"
    SQLALCHEMY = "sentry_sdk.integrations.sqlalchemy.SqlalchemyIntegration"

    def import_integration(self) -> Integration:
        module_name, class_name = self.rsplit(".", 1)
        module = importlib.import_module(module_name)
        integration_class: type[Integration] = getattr(module, class_name)

        if self is IntegrationImportsEnum.LOGGING:
            integration_class: type[LoggingIntegration]  # type: ignore[no-redef]
            return integration_class(level=logging.DEBUG, event_level=logging.WARNING)  # type: ignore[call-arg]

        return integration_class()
