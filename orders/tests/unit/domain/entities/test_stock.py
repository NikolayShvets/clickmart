from collections.abc import Callable
from decimal import Decimal

import pytest

from domain.entities import OrderItem, Product, Stock
from domain.exceptions import (
    AllocationMismatchError,
    OutOfStockError,
    StockIsBelowZeroError,
)


def test_create_stock_with_positive_quantity__ok(
    product_factory: Callable[..., Product],
    stock_factory: Callable[..., Stock],
) -> None:
    """Stock should be created with positive quantity."""
    product = product_factory()
    stock = stock_factory(product=product, quantity=10)

    assert stock.product == product
    assert stock.quantity == 10


def test_create_stock_with_zero_quantity__ok(
    product_factory: Callable[..., Product],
    stock_factory: Callable[..., Stock],
) -> None:
    """Stock should be created with zero quantity."""
    product = product_factory()
    stock = stock_factory(product=product, quantity=0)

    assert stock.quantity == 0


def test_create_stock_with_negative_quantity__error(
    product_factory: Callable[..., Product],
    stock_factory: Callable[..., Stock],
) -> None:
    """Stock should not be created with negative quantity."""
    product = product_factory()

    with pytest.raises(StockIsBelowZeroError):
        stock_factory(product=product, quantity=-1)


def test_allocate_with_matching_sku__ok(
    product_factory: Callable[..., Product],
    stock_factory: Callable[..., Stock],
    order_item_factory: Callable[..., OrderItem],
) -> None:
    """Stock should be allocated when SKUs match and quantity is available."""
    product = product_factory()
    stock = stock_factory(product=product, quantity=10)
    order_item = order_item_factory(product=product, quantity=5)
    stock.allocate(order_item)

    assert stock.quantity == 5


def test_allocate_with_non_matching_sku__error(
    product_factory: Callable[..., Product],
    stock_factory: Callable[..., Stock],
    order_item_factory: Callable[..., OrderItem],
) -> None:
    """Stock should not be allocated when SKUs don't match."""
    product = product_factory()
    stock = stock_factory(product=product, quantity=10)
    other_product = product_factory(sku="OTHER-SKU")
    order_item = order_item_factory(product=other_product, quantity=5)

    with pytest.raises(AllocationMismatchError):
        stock.allocate(order_item)

    assert stock.quantity == 10


def test_allocate_with_insufficient_quantity__error(
    product_factory: Callable[..., Product],
    stock_factory: Callable[..., Stock],
    order_item_factory: Callable[..., OrderItem],
) -> None:
    """Stock should not be allocated when quantity is insufficient."""
    product = product_factory()
    stock = stock_factory(product=product, quantity=10)
    order_item = order_item_factory(product=product, quantity=15)

    with pytest.raises(OutOfStockError):
        stock.allocate(order_item)

    assert stock.quantity == 10


def test_from_dict__ok(
    product_factory: Callable[..., Product],
) -> None:
    """Stock should be created from dictionary."""
    expected_product = product_factory(
        sku="TEST-SKU",
        name="Test Product",
        description="Test Description",
        price=Decimal("10.00"),
    )
    data = {
        "product": {
            "sku": "TEST-SKU",
            "name": "Test Product",
            "description": "Test Description",
            "price": "10.00",
        },
        "quantity": 10,
    }
    stock = Stock.from_dict(data)

    assert stock.product.sku == expected_product.sku
    assert stock.product.name == expected_product.name
    assert stock.product.description == expected_product.description
    assert stock.product.price == expected_product.price
    assert stock.quantity == 10
