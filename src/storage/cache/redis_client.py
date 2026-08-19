import json
from typing import List, Dict, Any, Optional
import redis.asyncio as redis
from config.settings import get_settings


class RedisCache:
    """Redis client for sub-millisecond round caching and recent feed management."""

    def __init__(self):
        settings = get_settings()
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password or None,
            decode_responses=True
        )
        self.max_size = settings.cache_size

    async def push_round(self, round_data: Dict[str, Any]):
        key = "crash:recent_rounds"
        serialized = json.dumps(round_data, default=str)
        await self.client.lpush(key, serialized)
        await self.client.ltrim(key, 0, self.max_size - 1)

    async def get_recent_rounds(self, count: int = 50) -> List[Dict[str, Any]]:
        key = "crash:recent_rounds"
        items = await self.client.lrange(key, 0, count - 1)
        return [json.loads(item) for item in items]

    async def close(self):
        await self.client.close()
