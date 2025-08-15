from common.sentry.enums import ProfileLifecycleEnum
from common.shared.schemas import HttpsUrl
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["sentry_config"]


class SentryConfig(BaseSettings):
    enabled: bool
    dsn_url: HttpsUrl
    traces_sample_rate: float = Field(ge=0.0, le=1.0)
    profiles_sample_rate: float = Field(ge=0.0, le=1.0)
    profile_lifecycle: ProfileLifecycleEnum

    model_config = SettingsConfigDict(env_prefix="SENTRY_")


sentry_config = SentryConfig()
