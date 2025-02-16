from dataclasses import dataclass

from domain.value_objects.sku import SKU


@dataclass(frozen=True)
class OrderItemDTO:
    product_sku: SKU
    quantity: int
