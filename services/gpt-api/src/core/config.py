from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["service_config"]


class ServiceConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)

    model_config = SettingsConfigDict(env_prefix="GPT_API_")


service_config = ServiceConfig()
