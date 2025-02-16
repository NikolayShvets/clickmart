from application.uow import UoW
from domain.repositories import OrderRepository, StockRepository


class InMemoryUoW(UoW):
    def __init__(
        self,
        stock_repository: StockRepository,
        order_repository: OrderRepository,
    ) -> None:
        self.stock_repository = stock_repository
        self.order_repository = order_repository

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
