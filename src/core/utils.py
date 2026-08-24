import uuid
from datetime import datetime, timezone
from typing import Any, Dict


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_current_utc_timestamp() -> datetime:
    return datetime.now(timezone.utc)


def sanitize_float(value: Any, default: float = 1.00) -> float:
    try:
        val = float(value)
        return max(1.00, val)
    except (TypeError, ValueError):
        return default
