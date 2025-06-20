from common.environment.enums import EnvironmentEnum
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["env_config"]


class EnvConfig(BaseSettings):
    mode: EnvironmentEnum

    model_config = SettingsConfigDict(env_prefix="ENV_")

    @property
    def debug(self) -> bool:
        return EnvironmentEnum.development == self.mode


env_config = EnvConfig()
