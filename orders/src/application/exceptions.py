from collections.abc import Iterable

from domain.value_objects.sku import SKU


class ApplicationError(Exception):
    pass


class StockNotFoundError(ApplicationError):
    def __init__(self, product_skus: Iterable[SKU]) -> None:
        self._product_skus = product_skus

    def __str__(self) -> str:
        return f"Stock not found for product skus: {self._product_skus}"
