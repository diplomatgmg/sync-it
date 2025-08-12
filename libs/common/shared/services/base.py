from typing import TypeVar

from common.shared.repositories import BaseRepository
from common.shared.unitofwork import BaseUnitOfWork


__all__ = ["BaseService", "BaseUOWService"]


RepoType = TypeVar("RepoType", bound=BaseRepository)


class BaseService[RepoType: BaseRepository]:  # noqa: B903 Class could be dataclass or namedtuple
    """Базовый сервис для работы с репозиториями.

    Usage:
    >>> class ExampleService(BaseService[ExampleRepository]):
    >>>     pass
    """

    def __init__(self, repo: RepoType) -> None:
        self._repo = repo


UnitOfWorkType = TypeVar("UnitOfWorkType", bound=BaseUnitOfWork)


class BaseUOWService[UnitOfWorkType: BaseUnitOfWork]:  # noqa: B903 Class could be dataclass or namedtuple
    def __init__(self, uow: UnitOfWorkType) -> None:
        self._uow = uow
