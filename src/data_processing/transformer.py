from datetime import datetime
from typing import Dict, Any
from config.constants import MultiplierCategory


class DataTransformer:
    """Transforms cleaned round records into structured analytical formats."""

    @staticmethod
    def categorize_multiplier(multiplier: float) -> str:
        if multiplier < 2.0:
            return MultiplierCategory.LOW
        elif multiplier < 10.0:
            return MultiplierCategory.MEDIUM
        else:
            return MultiplierCategory.HIGH

    @classmethod
    def transform(cls, cleaned_data: Dict[str, Any]) -> Dict[str, Any]:
        multiplier = cleaned_data["multiplier"]
        category = cls.categorize_multiplier(multiplier)

        return {
            **cleaned_data,
            "category": category,
            "is_above_two": multiplier >= 2.0,
            "is_above_ten": multiplier >= 10.0,
            "processed_at": datetime.utcnow().isoformat(),
        }
