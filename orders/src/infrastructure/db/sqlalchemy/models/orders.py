from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.order import OrderStatus
from infrastructure.db.sqlalchemy.models.base import Base


class Orders(Base):
    number: Mapped[str] = mapped_column(String, unique=True, index=True)
    customer_id: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))

    def __str__(self) -> str:
        return (
            f"Order(number={self.number}, "
            f"customer_id={self.customer_id}, "
            f"status={self.status})"
        )
