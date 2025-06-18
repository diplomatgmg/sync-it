import hashlib


__all__ = ["generate_hash"]


def generate_hash(value: str, algorithm: str = "md5") -> str:
    """Генерирует хеш на основе переданного значения и алгоритма."""
    hasher = hashlib.new(algorithm)
    hasher.update(value.encode("utf-8"))

    return hasher.hexdigest()
