from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    app_name: str = "Green Gold Crash Engine"
    environment: str = "development"
    debug: bool = True

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "green_gold"
    postgres_user: str = "postgres"
    postgres_password: str = "secure_postgres_password"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    # InfluxDB
    influx_url: str = "http://localhost:8086"
    influx_token: str = "your_influx_super_secret_token"
    influx_org: str = "green-gold"
    influx_bucket: str = "crash_rounds"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    prometheus_port: int = 9090

    # Application Logic
    cache_size: int = 100
    retention_days: int = 365

    # Data Collection
    proxies: List[str] = Field(default_factory=list)
    user_agents: List[str] = Field(default_factory=lambda: [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    ])
    target_url: str = "https://example.com/aviator"

    @property
    def async_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def sync_postgres_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
