from dataclasses import dataclass
from enum import StrEnum

from domain.entities.order_item import OrderItem
from domain.exceptions import EmptyOrderError
from domain.value_objects.money import Money


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Order:
    customer_id: str
    status: OrderStatus
    items: list[OrderItem]

    def __post_init__(self) -> None:
        if not self.items:
            raise EmptyOrderError

    @property
    def total_price(self) -> Money:
        return sum(
            (item.total_price for item in self.items),
            Money.from_str("0"),
        )
