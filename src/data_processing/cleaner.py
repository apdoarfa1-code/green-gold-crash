from typing import Dict, Any
from src.core.exceptions import CleaningError
from src.core.utils import sanitize_float


class DataCleaner:
    """Validates and cleans incoming round payloads."""

    @staticmethod
    def clean(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(raw_data, dict):
            raise CleaningError("Raw data must be a dictionary.")

        multiplier = sanitize_float(raw_data.get("multiplier", 1.00))
        round_id = str(raw_data.get("round_id", ""))

        if not round_id:
            raise CleaningError("Missing round_id in payload.")

        return {
            "round_id": round_id,
            "multiplier": multiplier,
            "server_seed": raw_data.get("server_seed"),
            "client_seed": raw_data.get("client_seed"),
            "hash_value": raw_data.get("hash_value") or raw_data.get("hash"),
            "players_count": int(raw_data.get("players_count", 0)),
            "source": raw_data.get("source", "unknown"),
        }
