from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.sqlalchemy.models.base import Base


class Products(Base):
    sku: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(
        Numeric, CheckConstraint("price > 0")
    )

    def __str__(self) -> str:
        return f"Product(sku={self.sku}, name={self.name}, price={self.price})"
