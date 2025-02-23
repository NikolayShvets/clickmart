from dataclasses import dataclass
from typing import Any

from domain.entities.product import Product
from domain.exceptions import EmptyOrderItemError
from domain.value_objects.money import Money


@dataclass
class OrderItem:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise EmptyOrderItemError

    @property
    def total_price(self) -> Money:
        return self.product.price * self.quantity

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrderItem":
        return cls(
            product=Product.from_dict(data["product"]),
            quantity=data["quantity"],
        )
