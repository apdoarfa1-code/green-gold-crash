from typing import Dict, Any
from config.logging_config import logger
from src.core.events import event_bus
from src.data_processing.cleaner import DataCleaner
from src.data_processing.transformer import DataTransformer


class StreamProcessor:
    """Real-time stream pipeline processor subscribing to raw events."""

    def __init__(self):
        event_bus.subscribe("raw_data_collected", self.process_event)

    async def process_event(self, raw_data: Dict[str, Any]):
        try:
            # Handle websocket raw payload if needed or direct dictionary
            payload = raw_data.get("data", raw_data)
            if not isinstance(payload, dict):
                return

            cleaned = DataCleaner.clean(payload)
            transformed = DataTransformer.transform(cleaned)
            
            logger.debug(f"Stream processed round {transformed['round_id']} -> {transformed['multiplier']}x ({transformed['category']})")
            await event_bus.publish("round_processed", transformed)
        except Exception as e:
            logger.error(f"Stream processing error: {e}")


stream_processor = StreamProcessor()
