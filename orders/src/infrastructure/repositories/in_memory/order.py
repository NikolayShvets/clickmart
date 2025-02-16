from domain.entities import Order
from domain.repositories import OrderRepository
from domain.value_objects.order_number import OrderNumber


class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict[OrderNumber, Order] = {}

    async def get_by_number(self, number: OrderNumber) -> Order | None:
        return self._orders.get(number)

    async def create(self, order: Order) -> Order:
        self._orders[order.number] = order
        return order
