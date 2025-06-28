import re
from typing import Any

from common.logger import get_logger
from database.models.enums import GradeEnum
from utils.normalizers.normalize_profession import normalize_profession


__all__ = ["normalize_prompted_vacancy"]


logger = get_logger(__name__)


def normalize_prompted_vacancy(gpt_message: str) -> tuple[Any, ...] | None:
    if "Не вакансия" in gpt_message:
        return None

    normalized_message = _normalize_message(gpt_message)
    position = _extract_position(normalized_message)
    if position is None:
        logger.warning("Position not found in message: %s", normalized_message[:100])
        return None

    profession = _extract_profession(normalized_message)
    if profession is None:
        return None

    return position, profession


def _normalize_message(message: str) -> str:
    """Удаляет лишние символы из сообщения."""
    return message.replace("*", "").strip()


def _extract_position(message: str) -> GradeEnum | None:
    """Извлекает значение позиции из сообщения."""
    message = message.replace("+", "")

    pattern = r"Позиция:\s*(.*?)\n"
    match = re.search(pattern, message)
    if not match:
        return None

    position_str = match.group(1).strip().lower()
    return GradeEnum.get_safe(position_str)


def _extract_profession(message: str) -> str | None:
    """Извлекает значение профессии из сообщения."""
    pattern = r"Профессия:\s*(.*?)\n"
    match = re.search(pattern, message)
    if not match:
        return None

    profession_str = match.group(1).strip().lower()
    return normalize_profession(profession_str)
