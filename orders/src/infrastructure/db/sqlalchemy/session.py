from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

async_engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    if not async_session:
        raise RuntimeError("Database not initialized")

    async with async_session() as session:
        yield session
