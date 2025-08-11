from common.shared.schemas import HttpsUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["service_config"]


class ServiceConfig(BaseSettings):
    db_schema: str = "telegram_bot"

    token: str
    support_username: str
    rate_limit: float  # for throttling control in seconds
    use_webhook: bool
    webhook_url: HttpsUrl
    webhook_api_key: str

    model_config = SettingsConfigDict(env_prefix="TELEGRAM_BOT_")


service_config = ServiceConfig()
