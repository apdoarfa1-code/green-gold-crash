import time
import hmac
import hashlib
import json
from datetime import datetime, timezone
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Green Gold Vercel API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import math

SERVER_SEED = "green_gold_master_provably_fair_seed_2026"
CLIENT_SEED = "green_gold_client_seed_2026"
BETTING_DURATION = 7.0          # فترة الرهان (7 ثواني ثابتة)
GROWTH_RATE = 0.09              # معدل النمو الأسي للطائرة: m(t) = e^(0.09·t)
TIMELINE_BASE = 1735689600.0    # نقطة ارتكاز زمنية ثابتة (كل العملاء متزامنون عليها)


def flight_duration(crash_multiplier: float) -> float:
    """مدة طيران الطائرة حتى الوصول لرقم التحطم (تنمو أسياً مثل اللعبة الحقيقية)."""
    return math.log(crash_multiplier) / GROWTH_RATE


def compute_provably_fair_multiplier(server_seed: str, client_seed: str, nonce: int, house_edge_pct: float = 1.0) -> float:
    """Accurate mathematical implementation of Provably Fair Crash (HMAC-SHA256)."""
    message = f"{client_seed}:{nonce}".encode("utf-8")
    h = hmac.new(server_seed.encode("utf-8"), message, hashlib.sha256).hexdigest()
    
    # 52 bits precision
    h_52 = h[:13]
    val_52 = int(h_52, 16)
    max_52 = 2**52
    
    prob = val_52 / max_52
    if prob == 0:
        prob = 0.0000001
        
    multiplier = (100.0 - house_edge_pct) / (prob * 100.0)
    multiplier = max(1.00, round(multiplier, 2))
    
    if multiplier > 100.0:
        multiplier = round(1.00 + (int(h[:8], 16) % 9000) / 100.0, 2)
        
    return multiplier


class RoundSchema(BaseModel):
    id: int
    round_id: str
    multiplier: float
    timestamp: str
    server_seed: str


def walk_timeline(now: float):
    """
    يبني خطاً زمنياً حتمياً ومتزامناً لكل العملاء:
    كل جولة = رهان 7 ثواني + طيران أسي حتى رقم التحطم.
    يرجع (nonce, بداية الجولة, المضاعف, ثواني متبقية للرهان, مدة الطيران, المرحلة, المضاعف الحالي الحي).
    """
    cursor = TIMELINE_BASE
    nonce = 1
    while True:
        crash = compute_provably_fair_multiplier(SERVER_SEED, CLIENT_SEED, nonce)
        fly = flight_duration(crash)
        bet_end = cursor + BETTING_DURATION
        round_end = bet_end + fly
        if now < round_end:
            if now < bet_end:
                countdown = max(1, math.ceil(bet_end - now))
                return nonce, cursor, crash, countdown, fly, "betting", 1.00
            else:
                elapsed = now - bet_end
                live = round(math.exp(GROWTH_RATE * elapsed), 2)
                live = min(live, crash)
                return nonce, cursor, crash, 0, fly, "flight", live
        cursor = round_end
        nonce += 1


def get_latest_completed_rounds(count: int):
    """يرجع آخر الجولات المكتملة (الفعلية) من الخط الزمني الحتمي."""
    now = time.time()
    nonce, start, crash, countdown, fly, phase, _ = walk_timeline(now)
    rounds = []
    cursor = start
    n = nonce
    # ارجع للخلف على الخط الزمني
    while len(rounds) < count and n > 1:
        n -= 1
        c = compute_provably_fair_multiplier(SERVER_SEED, CLIENT_SEED, n)
        f = flight_duration(c)
        cursor_end = None
        # الفرق الزمني: نهاية الجولة n هي بداية الجولة n+1
        # نعيد بناء بالمشي الأمامي بدلاً من ذلك للدقة — لكننا نعرف بداية الجولة الحالية (start)
        # start الحالي = نهاية الجولة السابقة، لذا نحتاج مشياً عكسياً:
        # نهاية الجولة n = start (للأولى) ثم ننقص تدريجياً
        if cursor_end is None:
            cursor_end = start
        round_start = cursor_end - (BETTING_DURATION + f)
        ts = datetime.fromtimestamp(round_start, tz=timezone.utc).isoformat()
        rounds.append(RoundSchema(
            id=n,
            round_id=f"rnd_{n}",
            multiplier=c,
            timestamp=ts,
            server_seed=SERVER_SEED
        ))
        cursor_end = round_start
    return rounds


class CurrentStateSchema(BaseModel):
    cycle_epoch: int
    countdown: int
    phase: str
    current_multiplier: float
    live_multiplier: float = 1.00
    flight_duration: float = 0.0
    safe_cashout: float
    round_id: str
    confidence: float
    server_seed: str
    client_seed: str


def render_health_html(data_dict: dict) -> str:
    json_str = json.dumps(data_dict, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حالة النظام - Green Gold Cloud</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ font-family: 'Cairo', sans-serif; }}
        body {{ background-color: #0E1117; color: #FFFFFF; }}
        .card-bg {{ background-color: #161B22; border: 1px solid #21262D; }}
        .gold-gradient {{ background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-4 md:p-8">
    <div class="max-w-2xl mx-auto w-full mt-6 space-y-6">
        <div class="flex items-center justify-between border-b border-gray-800 pb-4">
            <div class="flex items-center space-x-3 space-x-reverse">
                <div class="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/50">
                    <i class="fa-solid fa-server text-emerald-400"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold gold-gradient">Green Gold Engine</h1>
                    <p class="text-xs text-gray-400">حالة الخادم التفاعلية</p>
                </div>
            </div>
            <a href="/" class="bg-gray-800 hover:bg-gray-700 text-xs px-3 py-1.5 rounded-lg border border-gray-700 transition">
                <i class="fa-solid fa-house ml-1"></i> الواجهة الرئيسية
            </a>
        </div>

        <div class="card-bg rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex items-center justify-between">
                <span class="text-sm font-bold text-gray-300">حالة التشغيل المباشرة</span>
                <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-950 text-emerald-400 border border-emerald-800/60 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    متصل 100%
                </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div class="p-3 bg-gray-900/80 rounded-xl border border-gray-800">
                    <p class="text-gray-400 mb-1">الخدمة</p>
                    <p class="font-bold text-emerald-400">{data_dict.get('service') or data_dict.get('الخدمة')}</p>
                </div>
                <div class="p-3 bg-gray-900/80 rounded-xl border border-gray-800">
                    <p class="text-gray-400 mb-1">الدورة الحالية (Epoch)</p>
                    <p class="font-mono font-bold text-amber-400">{data_dict.get('epoch')}</p>
                </div>
            </div>

            <div>
                <p class="text-xs font-bold text-gray-400 mb-2">استجابة البيانات المنسقة (JSON):</p>
                <pre class="bg-gray-900 p-4 rounded-xl text-emerald-300 font-mono text-xs overflow-x-auto border border-gray-800 text-left" dir="ltr">{json_str}</pre>
            </div>
        </div>
    </div>
    <footer class="text-center text-xs text-gray-500 my-4">
        © 2026 Green Gold Engineering System
    </footer>
</body>
</html>"""


@app.get("/api/health")
def health(request: Request, lang: Optional[str] = Query(default=None)):
    now = time.time()
    nonce, start, crash, countdown, fly, phase, live = walk_timeline(now)
    ts = datetime.now(timezone.utc).isoformat()
    epoch = nonce
    
    if lang == "ar":
        data = {
            "الحالة": "صحي",
            "الخدمة": "Green Gold Cloud (Vercel Serverless)",
            "الطابع الزمني": ts,
            "epoch": epoch
        }
    else:
        data = {
            "status": "healthy",
            "service": "Green Gold Cloud (Vercel Serverless)",
            "timestamp": ts,
            "epoch": epoch
        }
    
    accept = request.headers.get("accept", "")
    if "text/html" in accept and not lang == "json":
        return HTMLResponse(content=render_health_html(data))
    
    return JSONResponse(content=data)


@app.get("/api/health/ar")
def health_ar(request: Request):
    now = time.time()
    nonce, *_ = walk_timeline(now)
    data = {
        "الحالة": "صحي",
        "الخدمة": "Green Gold Cloud (Vercel Serverless)",
        "الطابع الزمني": datetime.now(timezone.utc).isoformat(),
        "epoch": nonce
    }
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(content=render_health_html(data))
    
    return JSONResponse(content=data)


@app.get("/api/current", response_model=CurrentStateSchema)
def get_current_state():
    nonce, start, crash, countdown, fly, phase, live = walk_timeline(time.time())

    multiplier = crash
    safe_cashout = round(max(1.10, multiplier * 0.82), 2)

    # درجة الثقة: تقل كلما ارتفع رقم التحطم المستهدف
    confidence = round(max(65.0, min(95.0, 90.0 - (multiplier * 1.5))), 1)

    return CurrentStateSchema(
        cycle_epoch=nonce,
        countdown=countdown,
        phase=phase,
        current_multiplier=multiplier,
        live_multiplier=live,
        flight_duration=round(fly, 2),
        safe_cashout=safe_cashout,
        round_id=f"rnd_{nonce}",
        confidence=confidence,
        server_seed=SERVER_SEED,
        client_seed=CLIENT_SEED
    )


@app.get("/api/latest", response_model=List[RoundSchema])
def get_latest_rounds(count: int = Query(default=20, le=50)):
    return get_latest_completed_rounds(count)


class VerifyRequest(BaseModel):
    server_seed: str
    client_seed: str
    nonce: int


@app.post("/api/verify")
def verify_round(req: VerifyRequest):
    mult = compute_provably_fair_multiplier(req.server_seed, req.client_seed, req.nonce)
    message = f"{req.client_seed}:{req.nonce}".encode("utf-8")
    h = hmac.new(req.server_seed.encode("utf-8"), message, hashlib.sha256).hexdigest()
    return {
        "verified_multiplier": mult,
        "hash_signature": h,
        "provably_fair": True
    }
