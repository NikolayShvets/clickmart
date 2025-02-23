from dataclasses import dataclass
from typing import Any

from domain.value_objects.money import Money
from domain.value_objects.sku import SKU


@dataclass
class Product:
    sku: SKU
    name: str
    description: str
    price: Money

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return False

        return self.sku == other.sku

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Product":
        return cls(
            sku=SKU(data["sku"]),
            name=data["name"],
            description=data["description"],
            price=Money.from_str(data["price"]),
        )
