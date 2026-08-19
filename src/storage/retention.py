from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from src.storage.postgres.models import RoundModel
from config.logging_config import logger


class DataRetentionManager:
    """Manages automatic archival and pruning of historical records based on retention days."""

    def __init__(self, session: AsyncSession, retention_days: int = 365):
        self.session = session
        self.retention_days = retention_days

    async def prune_old_rounds(self) -> int:
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
        stmt = delete(RoundModel).where(RoundModel.timestamp < cutoff_date)
        result = await self.session.execute(stmt)
        await self.session.commit()
        deleted_count = result.rowcount
        logger.info(f"Pruned {deleted_count} rounds older than {self.retention_days} days.")
        return deleted_count
