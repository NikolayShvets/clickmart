from typing import TYPE_CHECKING
from uuid import UUID as PYUUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from infrastructure.sqlalchemy.models.products import Products


class Stocks(Base):
    product_id: Mapped[PYUUID] = mapped_column(
        ForeignKey("products.id"), index=True
    )
    quantity: Mapped[int] = mapped_column(
        CheckConstraint("quantity >= 0"), nullable=False
    )

    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="stocks",
    )

    def __str__(self) -> str:
        return f"Stock(product_id={self.product_id}, quantity={self.quantity})"
