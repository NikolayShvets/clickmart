from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from infrastructure.sqlalchemy.models.order_items import OrderItems
    from infrastructure.sqlalchemy.models.stocks import Stocks


class Products(Base):
    sku: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(
        Numeric, CheckConstraint("price > 0")
    )

    stocks: Mapped[list["Stocks"]] = relationship(
        "Stocks",
        back_populates="product",
    )
    order_items: Mapped[list["OrderItems"]] = relationship(
        "OrderItems",
        back_populates="product",
    )

    def __str__(self) -> str:
        return f"Product(sku={self.sku}, name={self.name}, price={self.price})"
