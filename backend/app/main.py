import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime, timezone
from app.provably_fair import ProvablyFairSimulator


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        # Iterate over a snapshot to avoid mutation during broadcast
        for connection in list(self.active_connections):
            try:
                await connection.send_json(data)
            except Exception:
                self.disconnect(connection)


manager = ConnectionManager()


# Server state
_ROUNDS = []
_SERVER_SEED = "green_gold_master_provably_fair_seed_2026"
_CLIENT_SEED = "green_gold_client_seed_2026"


async def game_round_generator():
    """Generates a new Provably Fair round every 7 seconds, strictly aligned to the wall clock."""
    global _ROUNDS
    import time
    # Start nonce after the 10 seeded rounds to avoid duplicate round_ids
    nonce = 11

    # Initialize some rounds on startup (nonce 1..10)
    for i in range(10, 0, -1):
        multiplier = ProvablyFairSimulator.generate_round(_SERVER_SEED, _CLIENT_SEED, i)
        _ROUNDS.append({
            "id": 11 - i,
            "multiplier": multiplier,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "server_seed": _SERVER_SEED,
            "round_id": f"rnd_{i}"
        })
    
    while True:
        nonce += 1
        multiplier = ProvablyFairSimulator.generate_round(_SERVER_SEED, _CLIENT_SEED, nonce)
        new_round = {
            "id": len(_ROUNDS) + 1,
            "multiplier": multiplier,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "server_seed": _SERVER_SEED,
            "round_id": f"rnd_{nonce}"
        }
        _ROUNDS.insert(0, new_round)
        if len(_ROUNDS) > 200:
            _ROUNDS.pop()
        await manager.broadcast({"event": "new_round", "data": new_round})
        
        # Wait until the next exact 7-second boundary
        now = time.time()
        sleep_time = 7.0 - (now % 7.0)
        await asyncio.sleep(sleep_time)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(game_round_generator())
    yield
    task.cancel()


app = FastAPI(title="Green Gold Cloud Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    import time
    now = time.time()
    cycle_epoch = int(now // 7)
    time_in_cycle = now % 7
    return {
        "status": "healthy",
        "service": "Green Gold Render Backend",
        "current_cycle": cycle_epoch,
        "seconds_until_next_round": round(7.0 - time_in_cycle, 2)
    }


@app.get("/api/latest")
async def get_latest_rounds(count: int = Query(default=50, le=100)):
    return _ROUNDS[:count]


@app.get("/api/stats")
async def get_statistics():
    if not _ROUNDS:
        return {"average": 1.0, "max": 1.0, "count": 0}
    mults = [r["multiplier"] for r in _ROUNDS]
    return {
        "average": round(sum(mults) / len(mults), 2),
        "max": max(mults),
        "count": len(mults)
    }


@app.get("/api/current")
async def get_current_round():
    """Returns the active round + countdown state for the next round."""
    import time
    now = time.time()
    cycle_epoch = int(now // 7)
    time_in_cycle = now % 7
    countdown = 7 - int(time_in_cycle)
    if countdown == 0:
        countdown = 1
    
    if not _ROUNDS:
        return {}
    
    current = _ROUNDS[0]
    safe_cashout = round(current["multiplier"] * 0.82, 2)
    
    return {
        "current": current,
        "safe_cashout": safe_cashout,
        "countdown": countdown,
        "cycle_epoch": cycle_epoch,
        "phase": "betting" if time_in_cycle < 7.0 else "flight"
    }


@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
