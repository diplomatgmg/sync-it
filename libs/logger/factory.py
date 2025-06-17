import inspect
import logging
import sys

from libs.logger.config import log_config


__all__ = ["get_logger"]


_original_get_logger = logging.getLogger


def get_logger(name: str | None = None) -> logging.Logger:
    logger = _original_get_logger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(log_config.level.value)

    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_config.level.value)

    logger.addHandler(console_handler)

    return logger


def _get_logger_wrapper(name: str | None = None) -> logging.Logger:
    """Выведет сообщение, если вызвали logging.getLogger() внутри проекта вместо get_logger()"""
    stack = inspect.stack()

    for frame_info in stack[1:]:
        filename = frame_info.filename

        if "site-packages" in filename or "local/lib" in filename:
            break

        if not getattr(_get_logger_wrapper, "_warned", False):
            logging.warning(  # noqa: LOG015
                "Use libs.logging.get_logger() instead logging.getLogger() в %s",
                filename,
            )
            _get_logger_wrapper._warned = True  # type: ignore[attr-defined]  # noqa: SLF001

        break

    return get_logger(name)


logging.getLogger = _get_logger_wrapper
