from datetime import datetime
from typing import Dict, Any, Optional
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from config.settings import get_settings
from config.logging_config import logger


class InfluxTimeSeriesClient:
    """Client for writing and querying high-frequency round data in InfluxDB."""

    def __init__(self):
        settings = get_settings()
        self.url = settings.influx_url
        self.token = settings.influx_token
        self.org = settings.influx_org
        self.bucket = settings.influx_bucket
        self.client: Optional[InfluxDBClient] = None
        self.write_api = None

        try:
            self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        except Exception as e:
            logger.warning(f"Failed to initialize InfluxDB client: {e}")

    def write_round(self, round_data: Dict[str, Any]):
        if not self.write_api:
            return
        try:
            point = (
                Point("crash_round")
                .tag("round_id", round_data.get("round_id"))
                .tag("source", round_data.get("source", "unknown"))
                .field("multiplier", float(round_data.get("multiplier", 1.00)))
                .field("players_count", int(round_data.get("players_count", 0)))
                .time(datetime.utcnow())
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        except Exception as e:
            logger.error(f"Error writing to InfluxDB: {e}")

    def close(self):
        if self.client:
            self.client.close()
