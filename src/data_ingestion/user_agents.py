import random
from typing import List, Optional
from config.settings import get_settings


class UserAgentManager:
    """Manages User-Agent rotation for anti-bot evasion."""

    def __init__(self, user_agents: Optional[List[str]] = None):
        settings = get_settings()
        self.user_agents = user_agents if user_agents is not None else settings.user_agents

    def get_random_user_agent(self) -> str:
        if not self.user_agents:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        return random.choice(self.user_agents)
