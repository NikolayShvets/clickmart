from dataclasses import dataclass

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
