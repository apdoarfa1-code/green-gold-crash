from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.round_schema import RoundResponse
from supabase import create_client, Client
import os

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


@router.get("/latest", response_model=List[RoundResponse])
async def get_latest_rounds(count: int = Query(default=50, le=100)):
    try:
        supabase = get_supabase()
        response = supabase.table("rounds").select("*").order("timestamp", desc=True).limit(count).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
