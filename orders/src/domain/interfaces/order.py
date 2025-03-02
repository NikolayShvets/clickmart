from abc import abstractmethod
from typing import Protocol

from domain.entities.order import Order
from domain.value_objects.order_number import OrderNumber


class OrderRepository(Protocol):
    @abstractmethod
    async def get_by_number(self, number: OrderNumber) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, order: Order) -> None:
        raise NotImplementedError
