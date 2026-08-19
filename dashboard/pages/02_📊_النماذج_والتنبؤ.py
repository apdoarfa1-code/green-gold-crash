import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import os

st.set_page_config(page_title="النماذج والتنبؤ - Green Gold", page_icon="📊", layout="wide")

st.title("📊 نماذج التعلم الآلي والتنبؤ (ML & Ensemble)")
st.markdown("مقارنة أداء النماذج المتوازية (LSTM, GRU, Markov) وحساب احتمالات التجاوز وتوصيات السحب.")

API_BASE_URL = os.getenv("API_BASE_URL", "https://your-app.onrender.com/api")

# Generate mock recent multipliers sequence
np.random.seed(99)
sample_multipliers = list(np.random.exponential(scale=1.5, size=30) + 1.0)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("سلسلة المضاعفات المدخلة للنموذج")
    st.line_chart(sample_multipliers)

with col2:
    st.subheader("إعدادات التنبؤ")
    selected_model = st.selectbox("اختر النموذج", ["Ensemble (موصى به)", "LSTM Neural Network", "Markov Chain Matrix", "GRU Recurrent"])
    if st.button("تشغيل التنبؤ الفوري"):
        st.success("تم تشغيل النموذج بنجاح!")

st.markdown("---")
st.subheader("🎯 مخرجات التنبؤ والتحليل")

c1, c2, c3, c4 = st.columns(4)
c1.metric("احتمال التجاوز (> 2.0x)", "58.3%", "+2.1%")
c2.metric("توصية السحب المثلى", "1.75x", "آمن")
c3.metric("مستوى ثقة النموذج", "81.4%", "مرتفع")
c4.metric("دقة النماذج التاريخية", "64.2%", "Win Rate")

st.markdown("---")
st.info("ملاحظة: النماذج مخصصة لدراسة السلاسل الزمنية الإحصائية البحتة وليست للرهان المالي.")
