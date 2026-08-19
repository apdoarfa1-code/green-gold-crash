import asyncio
from config.logging_config import logger
from src.core.events import event_bus
from src.data_ingestion.playwright_client import PlaywrightInterceptor
from src.data_ingestion.retry_handler import retry_on_exception


class DataCollectorService:
    """Orchestrates data collection streams and publishes events."""

    def __init__(self, target_url: str):
        self.interceptor = PlaywrightInterceptor(target_url)
        self.interceptor.on_data(self._handle_raw_data)

    async def _handle_raw_data(self, data: dict):
        logger.debug(f"Collected raw data: {data.get('source')}")
        await event_bus.publish("raw_data_collected", data)

    @retry_on_exception(max_attempts=3, delay=2.0)
    async def start_collection(self):
        logger.info("Initializing Data Collector Service...")
        await self.interceptor.start()
        await self.interceptor.navigate()

    async def stop_collection(self):
        await self.interceptor.close()
        logger.info("Data Collector Service stopped.")
