from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.entities import Order
from domain.interfaces import OrderRepository
from domain.value_objects.order_number import OrderNumber
from infrastructure.sqlalchemy.models import OrderItems, Orders


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # TODO: на вход и выход дто-шку
    async def get_by_number(self, number: OrderNumber) -> Order | None:
        query = (
            select(Orders)
            .where(Orders.number == number)
            .options(
                joinedload(Orders.items).joinedload(OrderItems.product),
            )
        )
        record = (await self._session.execute(query)).scalar_one_or_none()

        if record is None:
            return None

        # TODO: это так просто не работает, нужно
        # приджойненные модели так же переводить в словари.
        # Возможно, этого удастся избежать, если использовать
        # DTO вместо самих сущностей.
        # Либо нужно переделать метод to_dict
        return Order.from_dict(record.to_dict())

    async def create(self, order: Order) -> None:
        record = Orders(
            number=order.number.value,
            customer_id=order.customer_id,
            status=order.status,
        )
        self._session.add(record)
