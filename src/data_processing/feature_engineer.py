import numpy as np
import pandas as pd
from typing import List, Dict, Any


class FeatureEngineer:
    """Computes statistical features and sliding window metrics for ML models."""

    @staticmethod
    def compute_features(rounds: List[Dict[str, Any]], window_size: int = 10) -> pd.DataFrame:
        if not rounds:
            return pd.DataFrame()

        df = pd.DataFrame(rounds)
        if "multiplier" not in df.columns:
            return df

        # Rolling statistics
        df["rolling_mean"] = df["multiplier"].rolling(window=window_size, min_periods=1).mean()
        df["rolling_std"] = df["multiplier"].rolling(window=window_size, min_periods=1).std().fillna(0.0)
        df["rolling_max"] = df["multiplier"].rolling(window=window_size, min_periods=1).max()
        df["rolling_min"] = df["multiplier"].rolling(window=window_size, min_periods=1).min()

        # Lag features
        for lag in range(1, 4):
            df[f"lag_{lag}"] = df["multiplier"].shift(lag).fillna(1.00)

        # Binary threshold targets
        df["target_above_2"] = (df["multiplier"] >= 2.0).astype(int)

        return df
