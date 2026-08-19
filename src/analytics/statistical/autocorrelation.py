import numpy as np
from typing import List


class AutocorrelationAnalyzer:
    """Analyzes autocorrelation in multiplier time-series to test for memory patterns."""

    @staticmethod
    def compute_acf(multipliers: List[float], nlags: int = 10) -> List[float]:
        if len(multipliers) <= nlags:
            return []

        arr = np.array(multipliers)
        mean = np.mean(arr)
        c0 = np.sum((arr - mean) ** 2)

        if c0 == 0:
            return [0.0] * nlags

        acf_values = []
        for lag in range(1, nlags + 1):
            c_lag = np.sum((arr[:-lag] - mean) * (arr[lag:] - mean))
            acf_values.append(float(c_lag / c0))

        return acf_values
