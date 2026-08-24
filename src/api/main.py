from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings
from src.api.routes import rounds, predictions, statistics, health
from src.api.websockets.live_feed import websocket_endpoint
from src.storage.cache.redis_client import RedisCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = RedisCache()
    yield
    await app.state.cache.close()


settings = get_settings()
app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(rounds.router, prefix="/api/v1/rounds", tags=["Rounds"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["Predictions"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["Statistics"])
app.add_api_websocket_route("/ws/live", websocket_endpoint)
