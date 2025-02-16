from abc import abstractmethod
from types import TracebackType
from typing import Protocol

from domain.repositories import OrderRepository, StockRepository


class UoW(Protocol):
    stock_repository: StockRepository
    order_repository: OrderRepository

    async def __aenter__(self) -> "UoW":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        if exc_type is not None:
            await self.rollback()
            return False

        try:
            await self.commit()
        except Exception:
            await self.rollback()
            raise

        return True

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
