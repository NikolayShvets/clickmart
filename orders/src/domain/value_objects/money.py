from dataclasses import dataclass
from decimal import Decimal

from domain.exceptions import MoneyIsNotPositiveError


@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self) -> None:
        if self.amount <= Decimal("0.00"):
            raise MoneyIsNotPositiveError

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __mul__(self, multiplier: int) -> "Money":
        return Money(self.amount * multiplier)

    @staticmethod
    def from_str(amount: str) -> "Money":
        return Money(Decimal(amount))
