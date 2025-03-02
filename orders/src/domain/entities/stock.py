from dataclasses import dataclass
from typing import Any

from domain.entities.order_item import OrderItem
from domain.entities.product import Product
from domain.exceptions import (
    AllocationMismatchError,
    OutOfStockError,
    StockIsBelowZeroError,
)


@dataclass
class Stock:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise StockIsBelowZeroError

    def allocate(self, order_item: OrderItem) -> None:
        if order_item.product.sku != self.product.sku:
            raise AllocationMismatchError

        if self.quantity < order_item.quantity:
            raise OutOfStockError

        self.quantity -= order_item.quantity

    # TODO: очень неудобно работать с этим
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Stock":
        return cls(
            product=Product.from_dict(data["product"]),
            quantity=data["quantity"],
        )
