from collections.abc import Callable
from decimal import Decimal
from typing import Any

import pytest

from domain.entities import Order, OrderItem, Product, Stock
from domain.interfaces import DBSession, OrderRepository, StockRepository
from domain.value_objects import SKU, Money, OrderNumber


@pytest.fixture
def product_factory() -> Callable[..., Product]:
    """Фабрика для создания тестовых продуктов."""

    def _create(
        sku: str = "TEST-SKU",
        name: str = "Test Product",
        description: str = "Test Description",
        price: Decimal = Decimal("10.00"),
    ) -> Product:
        return Product(
            sku=SKU(sku),
            name=name,
            description=description,
            price=Money(price),
        )

    return _create


@pytest.fixture
def stock_factory() -> Callable[..., Stock]:
    """Фабрика для создания тестовых стоков."""

    def _create(
        product: Product,
        quantity: int = 10,
    ) -> Stock:
        return Stock(product=product, quantity=quantity)

    return _create


@pytest.fixture
def order_item_factory() -> Callable[..., OrderItem]:
    """Фабрика для создания тестовых заказов."""

    def _create(product: Product, quantity: int = 1) -> OrderItem:
        return OrderItem(product=product, quantity=quantity)

    return _create


class InMemorySession(DBSession):
    def __init__(
        self,
        storage: dict[str, Any],
    ) -> None:
        self.storage = storage
        self.dirty_storage: dict[str, Any] = {}

    async def commit(self) -> None:
        for key, value in self.dirty_storage.items():
            self.storage[key] = value
        self.dirty_storage.clear()

    async def flush(self) -> None:
        pass

    async def rollback(self) -> None:
        self.dirty_storage.clear()


class InMemoryStockRepository(StockRepository):
    def __init__(
        self,
        storage: dict[str, Stock],
    ) -> None:
        self._session = InMemorySession(storage)

    async def get_by_sku(self, product_sku: SKU) -> Stock | None:
        return self._session.storage.get(str(product_sku))

    async def update(self, stock: Stock) -> None:
        self._session.dirty_storage[str(stock.product.sku)] = stock


class InMemoryOrderRepository(OrderRepository):
    def __init__(self, storage: dict[str, Order]) -> None:
        self._session = InMemorySession(storage)

    async def get_by_number(self, number: OrderNumber) -> Order | None:
        return self._session.storage.get(str(number))

    async def create(self, order: Order) -> None:
        self._session.dirty_storage[str(order.number)] = order
