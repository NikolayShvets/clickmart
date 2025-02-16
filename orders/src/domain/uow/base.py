from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Generic, TypeVar, TypeVarTuple, Unpack, cast

from domain.repositories.base import Repository

R = TypeVar("R", bound=Repository[Any])
Repos = TypeVarTuple("Repos")


class UoW(ABC, Generic[Unpack[Repos]]):
    def __init__(
        self, repositories: dict[type[Repository[Any]], Repository[Any]]
    ) -> None:
        self._repositories = repositories

    async def __aenter__(self) -> "UoW[Unpack[Repos]]":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    def get_repository(self, repository_type: type[R]) -> R:
        repo = self._repositories[repository_type]
        return cast(R, repo)

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
