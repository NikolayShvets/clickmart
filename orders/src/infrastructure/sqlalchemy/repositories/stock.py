from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.entities import Stock
from domain.entities.product import Product
from domain.interfaces import StockRepository
from domain.value_objects.money import Money
from domain.value_objects.sku import SKU
from infrastructure.sqlalchemy.models import Products, Stocks


class SQLAlchemyStockRepository(StockRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # TODO: на вход и выход дто-шку
    async def get_by_sku(self, sku: SKU) -> Stock | None:
        query = (
            select(Stocks)
            .join(Products)
            .options(joinedload(Stocks.product))
            .where(Products.sku == sku.value)
        )
        record = (await self._session.execute(query)).scalars().one_or_none()

        if record is None:
            return None

        return Stock(
            product=Product(
                sku=SKU(record.product.sku),
                name=record.product.name,
                description=record.product.description,
                price=Money(record.product.price),
            ),
            quantity=record.quantity,
        )

    async def update(self, stock: Stock) -> None:
        subquery = (
            select(Products.id)
            .where(Products.sku == stock.product.sku.value)
            .scalar_subquery()
        )
        query = (
            update(Stocks)
            .where(Stocks.product_id == subquery)
            .values(quantity=stock.quantity)
        )
        await self._session.execute(query)
