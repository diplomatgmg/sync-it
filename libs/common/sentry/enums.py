from enum import StrEnum
import importlib

from sentry_sdk.integrations import Integration


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
        return integration_class()
