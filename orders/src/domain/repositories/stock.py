from abc import abstractmethod
from typing import Protocol, runtime_checkable

from domain.entities.stock import Stock
from domain.repositories.base import Repository
from domain.value_objects.sku import SKU


@runtime_checkable
class StockRepository(Repository[Stock], Protocol):
    @abstractmethod
    async def get_by_sku(self, product_sku: SKU) -> Stock | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, stock: Stock) -> Stock:
        raise NotImplementedError
