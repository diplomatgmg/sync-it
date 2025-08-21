from abc import ABC, abstractmethod


__all__ = ["AbstractFileReader"]


class AbstractFileReader(ABC):
    @staticmethod
    @abstractmethod
    def read(file_path: str) -> str:
        pass
