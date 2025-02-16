from application.dto import CreateOrderDTO
from application.exceptions import StockNotFoundError
from domain.entities import Order, OrderItem, OrderStatus, Product, Stock
from domain.exceptions import OutOfStockError
from domain.repositories import OrderRepository, StockRepository
from domain.uow import UoW
from domain.value_objects.sku import SKU


class CreateOrderUseCase:
    def __init__(
        self,
        uow: UoW[OrderRepository, StockRepository],
    ) -> None:
        self._uow = uow

    async def execute(self, dto: CreateOrderDTO) -> Order:
        async with self._uow as uow:
            stock_repository = uow.get_repository(StockRepository)
            order_repository = uow.get_repository(OrderRepository)

            stocks: list[Stock] = [
                stock
                for product_sku in dto.product_skus
                if (stock := await stock_repository.get_by_sku(product_sku))
                is not None
            ]

            missing_stocks = set(dto.product_skus) - set(
                stock.product.sku for stock in stocks
            )
            if missing_stocks:
                raise StockNotFoundError(missing_stocks)

            products: dict[SKU, Product] = {
                stock.product.sku: stock.product for stock in stocks
            }

            items = [
                OrderItem(
                    product=products[item.product_sku],
                    quantity=item.quantity,
                )
                for item in dto.items
            ]

            for stock, item in zip(stocks, items, strict=True):
                try:
                    stock.allocate(item)
                except OutOfStockError:
                    raise

            for stock in stocks:
                await stock_repository.update(stock)

            order = Order(
                customer_id=dto.customer_id,
                status=OrderStatus.PENDING,
                items=items,
            )
            return await order_repository.create(order)
