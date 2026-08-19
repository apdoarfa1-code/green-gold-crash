import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from src.analytics.ml_models.base import BaseModel


class LSTMModel(BaseModel):
    """Recurrent Neural Network (LSTM) for sequence prediction."""

    def __init__(self, sequence_length: int = 10, units: int = 32):
        self.sequence_length = sequence_length
        self.units = units
        self.model = self._build_model()

    def _build_model(self) -> Sequential:
        model = Sequential([
            LSTM(self.units, return_sequences=False, input_shape=(self.sequence_length, 1)),
            Dropout(0.2),
            Dense(16, activation="relu"),
            Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        return model

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 5, batch_size: int = 16) -> dict:
        history = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
        return {"loss": float(history.history["loss"][-1])}

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X, verbose=0)

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> dict:
        loss, accuracy = self.model.evaluate(X, y, verbose=0)
        return {"loss": float(loss), "accuracy": float(accuracy)}
