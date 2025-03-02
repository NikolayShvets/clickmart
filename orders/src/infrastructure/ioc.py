from collections.abc import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.use_cases import CreateOrderUseCase
from domain.interfaces import DBSession, OrderRepository, StockRepository
from infrastructure.repositories import (
    SQLAlchemyOrderRepository,
    SQLAlchemyStockRepository,
)
from infrastructure.settings import PostgreSQLSettings
from infrastructure.settings.postgresql import (
    get_settings as get_postgresql_settings,
)
from infrastructure.sqlalchemy.session import create_session_maker


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
    ) -> AsyncIterable[AnyOf[AsyncSession, DBSession]]:
        """Provide SQLAlchemy session."""
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def order_repository(self, session: AsyncSession) -> OrderRepository:
        """Provide order repository implementation."""
        return SQLAlchemyOrderRepository(session)

    @provide(scope=Scope.REQUEST)
    def stock_repository(self, session: AsyncSession) -> StockRepository:
        """Provide stock repository implementation."""
        return SQLAlchemyStockRepository(session)

    @provide(scope=Scope.REQUEST)
    def create_order_use_case(
        self,
        order_repository: OrderRepository,
        stock_repository: StockRepository,
        session: DBSession,
    ) -> CreateOrderUseCase:
        """Provide CreateOrderUseCase with injected UoW."""
        return CreateOrderUseCase(
            order_repository=order_repository,
            stock_repository=stock_repository,
            session=session,
        )
