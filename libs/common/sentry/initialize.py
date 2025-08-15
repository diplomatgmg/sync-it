from common.environment.config import env_config
from common.logger import get_logger
from common.sentry.config import sentry_config
from common.sentry.enums import IntegrationImportsEnum
import sentry_sdk


__all__ = ["init_sentry"]


logger = get_logger(__name__)


def init_sentry(integrations: list[IntegrationImportsEnum]) -> None:
    if not sentry_config.enabled:
        logger.info("Skip initializing Sentry")
        return

    logger.info("Initializing Sentry")

    sentry_sdk.init(
        dsn=str(sentry_config.dsn_url),
        integrations=[i.import_integration() for i in integrations],
        environment=env_config.mode,
        traces_sample_rate=sentry_config.traces_sample_rate,
        profile_lifecycle=sentry_config.profile_lifecycle.value,
    )
