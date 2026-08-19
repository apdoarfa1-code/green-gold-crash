import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, Any, List


class RegressionAnalyzer:
    """Applies regression modeling to study relationships with external factors."""

    @staticmethod
    def fit_linear_trend(multipliers: List[float]) -> Dict[str, Any]:
        if len(multipliers) < 2:
            return {"slope": 0.0, "intercept": 0.0, "score": 0.0}

        X = np.arange(len(multipliers)).reshape(-1, 1)
        y = np.array(multipliers)

        model = LinearRegression()
        model.fit(X, y)

        return {
            "slope": float(model.coef_[0]),
            "intercept": float(model.intercept_),
            "score": float(model.score(X, y))
        }
