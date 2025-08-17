from enum import StrEnum
import logging


__all__ = ["ProfileLifecycleEnum"]


logger = logging.getLogger(__name__)


class ProfileLifecycleEnum(StrEnum):
    MANUAL = "manual"
    TRACE = "trace"
