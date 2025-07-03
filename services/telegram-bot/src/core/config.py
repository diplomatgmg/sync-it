from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["service_config"]


class ServiceConfig(BaseSettings):
    db_schema: str = "telegram_bot"

    token: str

    model_config = SettingsConfigDict(env_prefix="TELEGRAM_BOT_")


service_config = ServiceConfig()
