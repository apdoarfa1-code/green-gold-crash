from abc import ABC, abstractmethod
import numpy as np


class BaseModel(ABC):
    """Abstract Base Class for all ML and analytical models."""

    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray) -> dict:
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> dict:
        pass
