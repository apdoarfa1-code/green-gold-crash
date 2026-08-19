import numpy as np
import scipy.stats as stats
from typing import List, Dict, Any


class DistributionAnalyzer:
    """Computes PDF, CDF, and distribution fitting for multiplier series."""

    @staticmethod
    def compute_summary_statistics(multipliers: List[float]) -> Dict[str, Any]:
        if not multipliers:
            return {}

        arr = np.array(multipliers)
        return {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "skewness": float(stats.skew(arr)),
            "kurtosis": float(stats.kurtosis(arr)),
        }

    @staticmethod
    def fit_exponential(multipliers: List[float]) -> Dict[str, float]:
        if not multipliers:
            return {}
        arr = np.array(multipliers)
        loc, scale = stats.expon.fit(arr)
        return {"loc": float(loc), "scale": float(scale)}
