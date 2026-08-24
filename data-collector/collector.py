import asyncio
import os
import json
import time
import random
from playwright.async_api import async_playwright
from uploader import SupabaseUploader


async def run_collector():
    print("🎯 Green Gold Live Collector Started")
    
    uploader = SupabaseUploader()
    
    # Target URL - المستخدم يقدر يغيرها للموقع الي عاوزه
    TARGET_URL = os.getenv("TARGET_URL", "https://example-crash-game.com")
    
    captured_rounds = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Intercept WebSocket Messages
        def handle_websocket(ws):
            print(f"✅ WebSocket connected: {ws.url}")
            ws.on("framereceived", lambda payload: asyncio.create_task(
                parse_ws_payload(payload, captured_rounds, uploader)
            ))
        
        # Intercept HTTP Responses
        async def handle_response(response):
            try:
                if any(kw in response.url.lower() for kw in ["crash", "round", "multiplier", "aviator", "game"]):
                    try:
                        body = await response.json()
                        if isinstance(body, dict):
                            mult = body.get("multiplier") or body.get("crash_point") or body.get("value")
                            rid = body.get("id") or body.get("round_id")
                            if mult and float(mult) >= 1.0 and rid:
                                round_data = {
                                    "round_id": str(rid),
                                    "multiplier": float(mult),
                                    "source": "playwright_live",
                                    "players_count": body.get("players_count", 0)
                                }
                                captured_rounds.append(round_data)
                                uploader.upload_round(round_data)
                                print(f"🚀 Captured Round: {rid} -> {mult}x")
                    except Exception:
                        pass
            except Exception:
                pass
        
        page.on("websocket", handle_websocket)
        page.on("response", lambda r: asyncio.create_task(handle_response(r)))
        
        try:
            print(f"🌐 Navigating to {TARGET_URL}")
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(60)  # اجمع جولات لدقيقة كاملة
        except Exception as e:
            print(f"⚠️ Error: {e}")
        
        await browser.close()
    
    if not captured_rounds:
        print("⚠️ No live data captured - Generating fallback round")
        uploader.upload_round({
            "round_id": f"rnd_fallback_{int(time.time())}",
            "multiplier": round(random.expovariate(1.0 / 1.5) + 1.0, 2),
            "players_count": random.randint(100, 3000),
            "source": "fallback_simulation"
        })


async def parse_ws_payload(payload, captured_rounds, uploader):
    try:
        data = json.loads(payload)
        if isinstance(data, dict):
            mult = data.get("multiplier") or data.get("crash_point") or data.get("value")
            rid = data.get("id") or data.get("round_id") or f"ws_{int(time.time())}"
            if mult and float(mult) >= 1.0:
                round_data = {
                    "round_id": str(rid),
                    "multiplier": float(mult),
                    "source": "playwright_ws",
                    "players_count": data.get("players_count", 0)
                }
                captured_rounds.append(round_data)
                uploader.upload_round(round_data)
                print(f"🚀 WS Captured: {rid} -> {mult}x")
    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(run_collector())
