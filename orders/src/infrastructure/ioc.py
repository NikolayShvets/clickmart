from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterator

from application.use_cases import CreateOrderUseCase
from domain.repositories import OrderRepository, StockRepository
from infrastructure.repositories.in_memory import InMemoryStockRepository
from infrastructure.repositories.sqlalchemy import SQLAlchemyOrderRepository
from infrastructure.settings import PostgreSQLSettings
from infrastructure.settings.postgresql import (
    get_settings as get_postgresql_settings,
)
from infrastructure.sqlalchemy.session import create_session_maker
from infrastructure.uow.in_memory import InMemoryUoW


class IoC(Provider):
    @provide(scope=Scope.APP)
    def get_postgresql_settings(self) -> PostgreSQLSettings:
        return get_postgresql_settings()

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, settings: PostgreSQLSettings
    ) -> async_sessionmaker[AsyncSession]:
        """Provide SQLAlchemy session maker."""
        return create_session_maker(settings)
    
    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        """Provide SQLAlchemy session."""
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def order_repository(self, session: AsyncSession) -> OrderRepository:
        """Provide order repository implementation."""
        return SQLAlchemyOrderRepository(session)

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
