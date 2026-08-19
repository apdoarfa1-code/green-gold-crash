import asyncio
from typing import Callable, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Request, Response
from config.logging_config import logger
from src.data_ingestion.proxy_manager import ProxyManager
from src.data_ingestion.user_agents import UserAgentManager


class PlaywrightInterceptor:
    """Advanced Playwright Client with Network Interception & WebSocket Listener."""

    def __init__(self, target_url: str):
        self.target_url = target_url
        self.proxy_manager = ProxyManager()
        self.ua_manager = UserAgentManager()
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.callbacks: list[Callable] = []

    async def start(self):
        proxy = self.proxy_manager.get_random_proxy()
        user_agent = self.ua_manager.get_random_user_agent()

        playwright_instance = await async_playwright().start()
        
        launch_args = {"headless": True}
        if proxy:
            launch_args["proxy"] = {"server": proxy}

        self.browser = await playwright_instance.chromium.launch(**launch_args)
        
        self.context = await self.browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1920, "height": 1080}
        )
        
        self.page = await self.context.new_page()
        self._setup_listeners()
        logger.info(f"Playwright started targeting {self.target_url} with UA: {user_agent[:30]}...")

    def _setup_listeners(self):
        if not self.page:
            return

        # Intercept HTTP Responses
        self.page.on("response", self._handle_response)
        
        # Intercept WebSocket traffic
        self.page.on("websocket", self._handle_websocket)

    async def _handle_response(self, response: Response):
        if "api" in response.url or "round" in response.url or "game" in response.url:
            try:
                data = await response.json()
                for cb in self.callbacks:
                    await cb({"source": "http", "url": response.url, "data": data})
            except Exception:
                pass

    async def _handle_websocket(self, ws):
        logger.info(f"WebSocket connected: {ws.url}")
        ws.on("framereceived", lambda payload: asyncio.create_task(
            self._dispatch_ws_frame(payload)
        ))

    async def _dispatch_ws_frame(self, payload: str):
        for cb in self.callbacks:
            try:
                await cb({"source": "websocket", "payload": payload})
            except Exception as e:
                logger.error(f"Error in WS callback: {e}")

    def on_data(self, callback: Callable):
        self.callbacks.append(callback)

    async def navigate(self):
        if self.page:
            await self.page.goto(self.target_url, wait_until="networkidle")

    async def close(self):
        if self.browser:
            await self.browser.close()
            logger.info("Playwright browser closed.")
