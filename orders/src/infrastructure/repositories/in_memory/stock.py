from domain.entities import Stock
from domain.repositories import StockRepository
from domain.value_objects.sku import SKU


class InMemoryStockRepository(StockRepository):
    def __init__(self) -> None:
        self._stocks: dict[SKU, Stock] = {}

    async def get_by_sku(self, product_sku: SKU) -> Stock | None:
        return self._stocks.get(product_sku)

    async def update(self, stock: Stock) -> Stock:
        self._stocks[stock.product.sku] = stock
        return stock
