import gymnasium as gym
from gymnasium import spaces
import numpy as np


class CrashEnvironment(gym.Env):
    """Custom Gymnasium environment simulating crash game mechanics and cash-out policies."""

    metadata = {"render_modes": ["human"]}

    def __init__(self, multipliers: np.ndarray = None):
        super().__init__()
        self.multipliers = multipliers if multipliers is not None else np.random.exponential(scale=2.0, size=1000) + 1.0
        self.current_step = 0
        
        # Action space: target cash-out multiplier (e.g. 1.1x to 10.0x)
        self.action_space = spaces.Box(low=1.01, high=10.0, shape=(1,), dtype=np.float32)
        
        # Observation space: recent multipliers history window
        self.observation_space = spaces.Box(low=1.0, high=100.0, shape=(10,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = np.random.randint(10, len(self.multipliers) - 1)
        obs = self.multipliers[self.current_step - 10:self.current_step]
        return obs, {}

    def step(self, action):
        target_cashout = float(action[0])
        actual_crash = float(self.multipliers[self.current_step])

        if target_cashout <= actual_crash:
            reward = target_cashout - 1.0
            terminated = True
        else:
            reward = -1.0
            terminated = True

        self.current_step += 1
        truncated = self.current_step >= len(self.multipliers) - 1
        
        obs = self.multipliers[self.current_step - 10:self.current_step] if not truncated else np.zeros(10)
        return obs, reward, terminated, truncated, {}
