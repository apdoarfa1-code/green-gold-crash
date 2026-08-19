import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import os
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Green Gold - Cloud Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st_autorefresh(interval=3000, key="homepage_autorefresh")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Sidebar
st.sidebar.markdown("### ✈️ Green Gold Cloud")
st.sidebar.markdown("---")

try:
    health_res = requests.get(f"{API_BASE_URL.replace('/api', '')}/api/health", timeout=2)
    if health_res.status_code == 200:
        st.sidebar.success("🟢 حالة الخادم: متصل")
    else:
        st.sidebar.warning("🟡 استجابة غير متوقعة")
except Exception:
    st.sidebar.error("🔴 الخادم غير متصل")

st.sidebar.markdown("---")
st.sidebar.info("نظام Green Gold المتكامل لتحليل بيانات كراش.")

st.title("✈️ Green Gold - نظام مراقبة وتحليل بيانات Aviator")

@st.cache_data(ttl=3)
def fetch_data():
    try:
        r = requests.get(f"{API_BASE_URL}/latest?count=50", timeout=3)
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json())
    except Exception:
        pass
    return pd.DataFrame()


df = fetch_data()

col1, col2, col3, col4 = st.columns(4)
if not df.empty:
    col1.metric("آخر مضاعف", f"{df.iloc[0]['multiplier']:.2f}x")
    col2.metric("أعلى مضاعف", f"{df['multiplier'].max():.2f}x")
    col3.metric("متوسط المضاعف", f"{df['multiplier'].mean():.2f}x")
    col4.metric("إجمالي الجولات", len(df))
else:
    col1.metric("آخر مضاعف", "1.00x")
    col2.metric("أعلى مضاعف", "1.00x")
    col3.metric("متوسط المضاعف", "1.00x")
    col4.metric("إجمالي الجولات", 0)

st.markdown("---")
st.subheader("📋 الجولات المسجلة من السيرفر")
if not df.empty:
    st.dataframe(df[["id", "round_id", "multiplier", "timestamp"]], use_container_width=True)
else:
    st.info("لا توجد جولات حالياً - تأكد من تشغيل Backend على بورت 8000")
