from domain.entities import Order
from domain.repositories import OrderRepository
from domain.value_objects.order_number import OrderNumber
from infrastructure.sqlalchemy.models import OrderItems, Orders
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

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

        return Order.from_dict(record.to_dict())

    async def create(self, order: Order) -> Order:
        # TODO: тут какая-то глупость, впустую гоняем сущность из словаря и обратно
        record = Orders(
            number=order.number,
            customer_id=order.customer_id,
            status=order.status,
        )
        self._session.add(record)
        await self._session.commit()
        await self._session.refresh(record)

        return Order.from_dict(record.to_dict())
