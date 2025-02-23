from uuid import UUID as PYUUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.sqlalchemy.models.base import Base


class Stocks(Base):
    product_id: Mapped[PYUUID] = mapped_column(
        ForeignKey("products.id"), index=True
    )
    quantity: Mapped[int] = mapped_column(
        CheckConstraint("quantity >= 0"), nullable=False
    )

    def __str__(self) -> str:
        return f"Stock(product_id={self.product_id}, quantity={self.quantity})"
