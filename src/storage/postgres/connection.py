from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config.settings import get_settings
from src.storage.postgres.models import Base

settings = get_settings()

engine = create_async_engine(settings.async_postgres_url, echo=settings.debug, future=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
