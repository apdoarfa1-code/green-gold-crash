from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer, DateTime, Index


class Base(DeclarativeBase):
    pass


class RoundModel(Base):
    __tablename__ = "rounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    round_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    multiplier: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    server_seed: Mapped[str] = mapped_column(String(256), nullable=True)
    client_seed: Mapped[str] = mapped_column(String(256), nullable=True)
    hash_value: Mapped[str] = mapped_column(String(128), nullable=True)
    players_count: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(64), default="unknown")

    __table_args__ = (
        Index("ix_round_timestamp_multiplier", "timestamp", "multiplier"),
    )
