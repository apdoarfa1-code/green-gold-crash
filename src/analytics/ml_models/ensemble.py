import numpy as np
from typing import List
from src.analytics.ml_models.base import BaseModel


class EnsembleModel(BaseModel):
    """Ensemble voting wrapper combining multiple model predictions."""

    def __init__(self, models: List[BaseModel], weights: List[float] = None):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)

    def train(self, X: np.ndarray, y: np.ndarray) -> dict:
        results = {}
        for i, model in enumerate(self.models):
            results[f"model_{i}"] = model.train(X, y)
        return results

    def predict(self, X: np.ndarray) -> np.ndarray:
        predictions = [model.predict(X) for model in self.models]
        weighted_preds = np.average(predictions, axis=0, weights=self.weights)
        return weighted_preds

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> dict:
        results = {}
        for i, model in enumerate(self.models):
            results[f"model_{i}"] = model.evaluate(X, y)
        return results
