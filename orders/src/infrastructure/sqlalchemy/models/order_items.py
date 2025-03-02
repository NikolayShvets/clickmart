from typing import TYPE_CHECKING
from uuid import UUID as PYUUID

from sqlalchemy import CheckConstraint, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from infrastructure.sqlalchemy.models.orders import Orders
    from infrastructure.sqlalchemy.models.products import Products


class OrderItems(Base):
    product_id: Mapped[PYUUID] = mapped_column(
        ForeignKey("products.id"),
        primary_key=True,
    )
    order_id: Mapped[PYUUID] = mapped_column(
        ForeignKey("orders.id"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("quantity > 0"),
        nullable=False,
    )

    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="order_items",
    )
    order: Mapped["Orders"] = relationship(
        "Orders",
        back_populates="items",
    )

    def __str__(self) -> str:
        return (
            f"OrderItem(product_id={self.product_id}, "
            f"order_id={self.order_id}, "
            f"quantity={self.quantity})"
        )
