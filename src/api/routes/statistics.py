from fastapi import APIRouter, Depends
from typing import List
from src.storage.cache.redis_client import RedisCache
from src.api.dependencies import get_cache
from src.analytics.statistical.distribution import DistributionAnalyzer
from src.analytics.statistical.autocorrelation import AutocorrelationAnalyzer

router = APIRouter()


@router.get("/summary")
async def get_statistics_summary(cache: RedisCache = Depends(get_cache)):
    recent = await cache.get_recent_rounds(100)
    multipliers = [r["multiplier"] for r in recent] if recent else [1.0, 1.5, 2.0, 1.2, 5.0]
    
    summary = DistributionAnalyzer.compute_summary_statistics(multipliers)
    acf = AutocorrelationAnalyzer.compute_acf(multipliers, nlags=5)
    
    return {
        "summary": summary,
        "autocorrelation": acf
    }
