from pathlib import Path

from utils.readers import AbstractFileReader


__all__ = ["TxtReader"]


class TxtReader(AbstractFileReader):
    @staticmethod
    def read(file_path: str) -> str:
        return Path(file_path).read_text(encoding="utf-8")
