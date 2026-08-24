from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.storage.postgres.models import RoundModel


class RoundRepository:
    """Repository pattern for managing round persistence in PostgreSQL."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_round(self, round_data: Dict[str, Any]) -> RoundModel:
        db_round = RoundModel(
            round_id=round_data["round_id"],
            multiplier=round_data["multiplier"],
            server_seed=round_data.get("server_seed"),
            client_seed=round_data.get("client_seed"),
            hash_value=round_data.get("hash_value"),
            players_count=round_data.get("players_count", 0),
            source=round_data.get("source", "unknown"),
        )
        self.session.add(db_round)
        await self.session.commit()
        await self.session.refresh(db_round)
        return db_round

    async def get_recent_rounds(self, limit: int = 100) -> List[RoundModel]:
        stmt = select(RoundModel).order_by(RoundModel.timestamp.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_round_id(self, round_id: str) -> Optional[RoundModel]:
        stmt = select(RoundModel).where(RoundModel.round_id == round_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
