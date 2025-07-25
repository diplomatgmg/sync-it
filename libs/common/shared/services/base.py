from typing import TypeVar

from common.shared.repositories import BaseRepository


__all__ = ["BaseService"]


RepoType = TypeVar("RepoType", bound=BaseRepository)


class BaseService[RepoType: BaseRepository]:  # noqa: B903 Class could be dataclass or namedtuple
    """Базовый сервис для работы с репозиториями.

    Usage:
    >>> class ExampleService(BaseService[ExampleRepository]):
    >>>     pass
    """

    def __init__(self, repo: RepoType) -> None:
        self._repo = repo
