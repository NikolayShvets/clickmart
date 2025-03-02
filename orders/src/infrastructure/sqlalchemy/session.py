from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infrastructure.settings.postgresql import PostgreSQLSettings


def create_session_maker(
    settings: PostgreSQLSettings,
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        settings.dsn,
        pool_size=15,
        max_overflow=15,
    )

    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
