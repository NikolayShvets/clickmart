from abc import abstractmethod
from typing import Protocol

from domain.entities.stock import Stock
from domain.value_objects.sku import SKU


class StockRepository(Protocol):
    @abstractmethod
    async def get_by_sku(self, product_sku: SKU) -> Stock | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, stock: Stock) -> None:
        raise NotImplementedError
