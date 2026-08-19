import asyncio
import json
from fastapi import WebSocket
from src.storage.cache.redis_client import RedisCache


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cache = RedisCache()
    try:
        last_item = None
        while True:
            recent = await cache.get_recent_rounds(1)
            if recent and recent[0] != last_item:
                last_item = recent[0]
                await websocket.send_text(json.dumps(last_item, default=str))
            await asyncio.sleep(0.5)
    except Exception:
        await websocket.close()
    finally:
        await cache.close()
