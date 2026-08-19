import streamlit as st
import pandas as pd
import requests
import os
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Green Gold - النظام المعتمد الحقيقي", page_icon="🎯", layout="centered")

# Ultra-fast 300ms refresh for seamless live sync with backend
st_autorefresh(interval=300, key="green_gold_ultimate_sync")

st.title("🎯 النظام المعتمد الحقيقي (100% متطابق مع السيرفر)")
st.markdown("مزامنة دقيقة مع خادم الـ Backend (بورت 8000) بدورة **7 ثوانٍ** كاملة: عداد رهان ➔ إقلاع ➔ تحطم.")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")


@st.cache_data(ttl=1)
def fetch_current_state():
    try:
        res = requests.get(f"{API_BASE_URL}/current", timeout=2)
        if res.status_code == 200 and res.json():
            return res.json()
    except Exception:
        pass
    return {}


@st.cache_data(ttl=2)
def fetch_backend_rounds():
    try:
        res = requests.get(f"{API_BASE_URL}/latest?count=20", timeout=2)
        if res.status_code == 200 and res.json():
            return res.json()
    except Exception:
        pass
    return []


# Get authoritative state directly from backend (single source of truth)
state = fetch_current_state()

if state and "current" in state:
    current_round = state["current"]
    current_multiplier = float(current_round["multiplier"])
    round_id = current_round["round_id"]
    countdown = int(state.get("countdown", 7))
    safe_cashout = float(state.get("safe_cashout", current_multiplier * 0.82))
else:
    # Backend unavailable - show clear warning
    current_multiplier = 1.00
    round_id = "offline"
    countdown = 7
    safe_cashout = 1.00

# --- STABLE UI DISPLAY ---
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="⏱️ العداد التنازلي للإقلاع",
        value=f"00:0{countdown} ثوانٍ",
        delta="مزامن من السيرفر"
    )

with col2:
    st.metric(
        label="🎯 الرقم المستهدف للجولة",
        value=f"{current_multiplier:.2f}x",
        delta=f"Round: {round_id}"
    )

with col3:
    st.metric(
        label="🛡️ نقطة السحب الآمن",
        value=f"{safe_cashout:.2f}x",
        delta="82% من الهدف"
    )

st.progress((8 - countdown) / 7.0)

if countdown > 1:
    st.info(f"⏳ **مرحلة الرهان مفتوحة**: متبقي **{countdown}** ثوانٍ. الجولة المستهدفة: `{round_id}` بمضاعف **{current_multiplier:.2f}x**")
else:
    st.success(f"🚀 **إقلاع وشيك الآن!** التنبؤ الثابت: **{current_multiplier:.2f}x** — السحب الآمن: **{safe_cashout:.2f}x**")

st.markdown("---")
st.subheader("📋 الجولات الحية من السيرفر")

backend_rounds = fetch_backend_rounds()
if backend_rounds:
    df_rounds = pd.DataFrame(backend_rounds)
    st.dataframe(df_rounds[["id", "round_id", "multiplier", "timestamp"]], use_container_width=True)
else:
    st.error("⚠️ لا يمكن الاتصال بخادم Backend على بورت 8000. تأكد من تشغيله.")
