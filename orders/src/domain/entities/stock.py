from dataclasses import dataclass

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
