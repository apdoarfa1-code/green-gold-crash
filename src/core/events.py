import asyncio
from typing import Callable, Dict, List, Any
from config.logging_config import logger


class EventBus:
    """In-memory Async Event Bus for decoupled publish/subscribe architecture."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed callback to event '{event_type}'")

    async def publish(self, event_type: str, data: Any):
        if event_type in self._subscribers:
            tasks = []
            for callback in self._subscribers[event_type]:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(asyncio.create_task(callback(data)))
                else:
                    callback(data)
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)


event_bus = EventBus()
