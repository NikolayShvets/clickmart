from abc import abstractmethod
from typing import Protocol, runtime_checkable

from domain.entities.order import Order
from domain.repositories.base import Repository
from domain.value_objects.sku import SKU


@runtime_checkable
class OrderRepository(Repository[Order], Protocol):
    @abstractmethod
    async def get_by_sku(self, sku: SKU) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def create(self, order: Order) -> Order:
        raise NotImplementedError
