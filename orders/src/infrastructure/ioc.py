from dishka import Provider, Scope, provide

from application.use_cases import CreateOrderUseCase
from domain.repositories import OrderRepository, StockRepository
from infrastructure.repositories.in_memory import (
    InMemoryOrderRepository,
    InMemoryStockRepository,
)
from infrastructure.uow.in_memory import InMemoryUoW


class IoC(Provider):
    @provide(scope=Scope.REQUEST)
    def order_repository(self) -> OrderRepository:
        """Provide order repository implementation."""
        return InMemoryOrderRepository()

    @provide(scope=Scope.REQUEST)
    def stock_repository(self) -> StockRepository:
        """Provide stock repository implementation."""
        return InMemoryStockRepository()

    @provide(scope=Scope.REQUEST)
    def unit_of_work(
        self,
        order_repository: OrderRepository,
        stock_repository: StockRepository,
    ) -> InMemoryUoW:
        """Provide UoW with injected repositories."""
        return InMemoryUoW(
            order_repository=order_repository,
            stock_repository=stock_repository,
        )

    @provide(scope=Scope.REQUEST)
    def create_order_use_case(self, uow: InMemoryUoW) -> CreateOrderUseCase:
        """Provide CreateOrderUseCase with injected UoW."""
        return CreateOrderUseCase(uow=uow)
