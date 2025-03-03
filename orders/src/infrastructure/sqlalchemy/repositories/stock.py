from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Stock
from domain.entities.product import Product
from domain.interfaces import StockRepository
from domain.value_objects import SKU, Money
from infrastructure.sqlalchemy.models import Products, Stocks


class SQLAlchemyStockRepository(StockRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # TODO: на вход и выход дто-шку
    async def get_by_sku(self, sku: SKU) -> Stock | None:
        # Сначала получаем Stock с блокировкой
        stock_query = (
            select(Stocks)
            .join(Products)
            .where(Products.sku == sku.value)
            .with_for_update()
        )
        stock_record = (
            await self._session.execute(stock_query)
        ).scalar_one_or_none()

        if stock_record is None:
            return None

        # Затем отдельно получаем Product
        product_query = select(Products).where(
            Products.id == stock_record.product_id
        )
        product_record = (
            await self._session.execute(product_query)
        ).scalar_one()

        return Stock(
            product=Product(
                sku=SKU(product_record.sku),
                name=product_record.name,
                description=product_record.description,
                price=Money(product_record.price),
            ),
            quantity=stock_record.quantity,
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
