from decimal import Decimal

import pytest

from domain.exceptions import MoneyIsNotPositiveError
from domain.value_objects.money import Money


def test_create_money_with_positive_amount__ok() -> None:
    """Money should be created with positive amount."""
    money = Money(Decimal("10.00"))
    assert money.amount == Decimal("10.00")


def test_create_money_with_zero_amount__error() -> None:
    """Money should not be created with zero amount."""
    with pytest.raises(MoneyIsNotPositiveError):
        Money(Decimal("0"))


def test_create_money_with_negative_amount__error() -> None:
    """Money should not be created with negative amount."""
    with pytest.raises(MoneyIsNotPositiveError):
        Money(Decimal("-10.00"))


def test_create_money_from_string__ok() -> None:
    """Money should be created from string."""
    money = Money.from_str("10.00")
    assert money.amount == Decimal("10.00")


def test_add_money__ok() -> None:
    """Money should be added to another Money."""
    money1 = Money(Decimal("10.00"))
    money2 = Money(Decimal("20.00"))
    result = money1 + money2
    assert result.amount == Decimal("30.00")


def test_multiply_money__ok() -> None:
    """Money should be multiplied by integer."""
    money = Money(Decimal("10.00"))
    result = money * 3
    assert result.amount == Decimal("30.00")
