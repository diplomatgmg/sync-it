import logging
import sys

from logger.config import log_config


__all__ = ["get_logger"]


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

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
