from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.order import OrderStatus
from infrastructure.sqlalchemy.models.base import Base
from infrastructure.sqlalchemy.models.order_items import OrderItems


class Orders(Base):
    number: Mapped[str] = mapped_column(String, unique=True, index=True)
    customer_id: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
    items: Mapped[list[OrderItems]] = relationship(
        "OrderItems",
        cascade="all, delete",
        back_populates="order",
    )

    def __str__(self) -> str:
        return (
            f"Order(number={self.number}, "
            f"customer_id={self.customer_id}, "
            f"status={self.status})"
        )
