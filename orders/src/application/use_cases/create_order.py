from uuid import uuid4

from application.dto import CreateOrderDTO, OrderItemDTO
from application.exceptions import StockNotFoundError
from application.uow import UoW
from domain.entities import Order, OrderItem, OrderStatus, Product, Stock
from domain.exceptions import OutOfStockError
from domain.value_objects.order_number import OrderNumber
from domain.value_objects.sku import SKU


class CreateOrderUseCase:
    def __init__(
        self,
        uow: UoW,
    ) -> None:
        self._uow = uow

    async def execute(self, dto: CreateOrderDTO) -> Order:
        async with self._uow:
            stocks = await self._get_stocks(dto.product_skus)
            self._validate_stocks_exist(dto.product_skus, stocks)

            products = self._create_products_map(stocks)
            items = self._create_order_items(dto.items, products)

            await self._allocate(stocks, items)
            await self._update_stocks(stocks)

            order = self._create_order(dto.customer_id, items)
            return await self._uow.order_repository.create(order)

    async def _get_stocks(self, product_skus: list[SKU]) -> list[Stock]:
        return [
            stock
            for sku in product_skus
            if (stock := await self._uow.stock_repository.get_by_sku(sku))
            is not None
        ]

    def _validate_stocks_exist(
        self,
        requested_skus: list[SKU],
        stocks: list[Stock],
    ) -> None:
        available_skus = {stock.product.sku for stock in stocks}
        missing_stocks = set(requested_skus) - available_skus
        if missing_stocks:
            raise StockNotFoundError(missing_stocks)

    def _create_products_map(self, stocks: list[Stock]) -> dict[SKU, Product]:
        return {stock.product.sku: stock.product for stock in stocks}

    def _create_order_items(
        self,
        items_dto: list[OrderItemDTO],
        products: dict[SKU, Product],
    ) -> list[OrderItem]:
        return [
            OrderItem(
                product=products[item.product_sku],
                quantity=item.quantity,
            )
            for item in items_dto
        ]

    async def _allocate(
        self,
        stocks: list[Stock],
        items: list[OrderItem],
    ) -> None:
        for stock, item in zip(stocks, items, strict=True):
            try:
                stock.allocate(item)
            except OutOfStockError:
                raise

    async def _update_stocks(self, stocks: list[Stock]) -> None:
        for stock in stocks:
            await self._uow.stock_repository.update(stock)

    def _create_order(
        self,
        customer_id: str,
        items: list[OrderItem],
    ) -> Order:
        return Order(
            number=OrderNumber(str(uuid4())),
            customer_id=customer_id,
            status=OrderStatus.PENDING,
            items=items,
        )
