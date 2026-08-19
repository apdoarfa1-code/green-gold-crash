from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Round(BaseModel):
    id: Optional[int] = None
    multiplier: float = Field(..., ge=1.00)
    timestamp: Optional[datetime] = None
    server_seed: Optional[str] = None
    client_seed: Optional[str] = None

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    average: float
    max: float
    count: int
