from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["api_config"]


class ApiConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)

    model_config = SettingsConfigDict(env_prefix="GPT_API_")


api_config = ApiConfig()
