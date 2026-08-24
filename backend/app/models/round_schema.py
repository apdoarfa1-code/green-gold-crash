from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RoundResponse(BaseModel):
    id: Optional[int] = None
    round_id: str
    multiplier: float = Field(..., ge=1.00)
    timestamp: datetime
    server_seed: Optional[str] = None
    client_seed: Optional[str] = None
    hash_value: Optional[str] = None
    players_count: Optional[int] = 0
    source: Optional[str] = "collector"

    class Config:
        from_attributes = True


class PredictionRequest(BaseModel):
    multipliers: list[float] = Field(..., min_length=5)


class PredictionResponse(BaseModel):
    model_name: str
    probability_above_2x: float
    recommended_cashout: float
    confidence: float
