import asyncio
from src.storage.postgres.connection import init_db
from config.logging_config import logger


async def main():
    logger.info("Initializing PostgreSQL Database and Tables...")
    await init_db()
    logger.info("Database initialization complete successfully.")


if __name__ == "__main__":
    asyncio.run(main())
