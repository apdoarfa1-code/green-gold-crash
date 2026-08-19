import os
import asyncpg
import numpy as np
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secure_postgres_password@localhost:5432/green_gold")


async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)


async def fetch_latest_rounds(limit: int = 50):
    try:
        conn = await get_db_connection()
        try:
            rows = await conn.fetch(
                "SELECT id, multiplier, timestamp, server_seed FROM rounds ORDER BY timestamp DESC LIMIT $1",
                limit
            )
            return [dict(row) for row in rows]
        finally:
            await conn.close()
    except Exception:
        # Fallback mock data when database is not reachable locally
        now = datetime.now(timezone.utc)
        mults = np.random.exponential(scale=1.6, size=limit) + 1.0
        return [
            {
                "id": i,
                "multiplier": round(float(mults[i-1]), 2),
                "timestamp": now,
                "server_seed": "mock_seed_hash"
            }
            for i in range(1, limit + 1)
        ]


async def fetch_stats():
    try:
        conn = await get_db_connection()
        try:
            row = await conn.fetchrow(
                "SELECT COALESCE(AVG(multiplier), 0.0) as avg, COALESCE(MAX(multiplier), 0.0) as max, COUNT(*) as count FROM rounds"
            )
            return {
                "average": float(row["avg"]),
                "max": float(row["max"]),
                "count": int(row["count"])
            }
        finally:
            await conn.close()
    except Exception:
        # Fallback mock stats
        return {
            "average": 1.75,
            "max": 14.50,
            "count": 100
        }
