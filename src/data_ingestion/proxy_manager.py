import random
from typing import List, Optional
from config.settings import get_settings


class ProxyManager:
    """Manages proxy rotation and selection for robust data scraping."""

    def __init__(self, proxies: Optional[List[str]] = None):
        settings = get_settings()
        self.proxies = proxies if proxies is not None else settings.proxies
        self._currentIndex = 0

    def get_random_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def get_next_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self._currentIndex]
        self._currentIndex = (self._currentIndex + 1) % len(self.proxies)
        return proxy
