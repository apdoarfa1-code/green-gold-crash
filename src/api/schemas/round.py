from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class RoundBase(BaseModel):
    round_id: str
    multiplier: float = Field(..., ge=1.00)
    server_seed: Optional[str] = None
    client_seed: Optional[str] = None
    hash_value: Optional[str] = None
    players_count: int = Field(default=0, ge=0)
    source: str = "unknown"


class RoundCreate(RoundBase):
    pass


class RoundResponse(RoundBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionRequest(BaseModel):
    multipliers: list[float] = Field(..., min_length=10)


class PredictionResponse(BaseModel):
    model_name: str
    probability_above_2x: float
    recommended_cashout: float
    confidence: float
