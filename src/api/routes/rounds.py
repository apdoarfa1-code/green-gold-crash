from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from src.api.schemas.round import RoundResponse, RoundCreate
from src.storage.cache.redis_client import RedisCache
from src.storage.postgres.repository import RoundRepository
from src.api.dependencies import get_cache, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/recent", response_model=List[RoundResponse])
async def get_recent_rounds(
    count: int = Query(default=50, le=100),
    cache: RedisCache = Depends(get_cache)
):
    rounds = await cache.get_recent_rounds(count)
    return rounds


@router.post("/", response_model=RoundResponse)
async def create_round(
    round_in: RoundCreate,
    session: AsyncSession = Depends(get_db_session),
    cache: RedisCache = Depends(get_cache)
):
    repo = RoundRepository(session)
    db_round = await repo.add_round(round_in.model_dump())
    
    # Push to redis cache
    await cache.push_round(round_in.model_dump())
    
    return db_round
