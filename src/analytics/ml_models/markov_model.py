import numpy as np
from src.analytics.ml_models.base import BaseModel


class MarkovChainModel(BaseModel):
    """Markov Chain transition matrix model across Low/Medium/High states."""

    def __init__(self, n_states: int = 3):
        self.n_states = n_states
        self.transition_matrix = np.zeros((n_states, n_states))

    def _discretize(self, multipliers: np.ndarray) -> np.ndarray:
        states = np.zeros(len(multipliers), dtype=int)
        states[multipliers < 2.0] = 0
        states[(multipliers >= 2.0) & (multipliers < 10.0)] = 1
        states[multipliers >= 10.0] = 2
        return states

    def train(self, X: np.ndarray, y: np.ndarray) -> dict:
        data = y.flatten() if len(y.shape) > 1 else y
        states = self._discretize(data)
        
        self.transition_matrix = np.zeros((self.n_states, self.n_states))
        for i in range(len(states) - 1):
            self.transition_matrix[states[i], states[i + 1]] += 1
            
        row_sums = self.transition_matrix.sum(axis=1, keepdims=True)
        self.transition_matrix = np.divide(self.transition_matrix, row_sums, where=row_sums != 0)
        
        return {"transition_matrix": self.transition_matrix.tolist()}

    def predict(self, X: np.ndarray) -> np.ndarray:
        if len(X) == 0:
            return np.array([1.0 / self.n_states] * self.n_states)
        last_val = X[-1]
        state = 0 if last_val < 2.0 else (1 if last_val < 10.0 else 2)
        return self.transition_matrix[state]

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> dict:
        return {"matrix_shape": list(self.transition_matrix.shape)}
