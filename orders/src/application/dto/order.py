from dataclasses import dataclass

from application.dto.order_item import OrderItemDTO
from domain.value_objects.sku import SKU


@dataclass(frozen=True)
class CreateOrderDTO:
    customer_id: str
    items: list[OrderItemDTO]

    @property
    def product_skus(self) -> list[SKU]:
        return [item.product_sku for item in self.items]
