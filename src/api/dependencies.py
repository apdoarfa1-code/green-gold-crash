from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.storage.postgres.connection import async_session_maker
from src.storage.cache.redis_client import RedisCache


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_cache() -> RedisCache:
    cache = RedisCache()
    try:
        yield cache
    finally:
        await cache.close()
