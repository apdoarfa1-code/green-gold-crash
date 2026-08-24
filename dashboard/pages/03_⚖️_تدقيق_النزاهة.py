import streamlit as st
import hmac
import hashlib

st.set_page_config(page_title="تدقيق النزاهة - Green Gold", page_icon="⚖️", layout="wide")

st.title("⚖️ تدقيق النزاهة الرياضية (Provably Fair)")
st.markdown("تحقق بنفسك من نزاهة أي جولة رياضياً باستخدام خوارزمية HMAC-SHA256 والبذور المشفرة.")


def compute_multiplier(server_seed: str, client_seed: str, nonce: int, house_edge_pct: float = 1.0) -> tuple:
    """نفس خوارزمية الخادم تماماً (52-bit Provably Fair)."""
    message = f"{client_seed}:{nonce}".encode("utf-8")
    h = hmac.new(server_seed.encode("utf-8"), message, hashlib.sha256).hexdigest()

    val_52 = int(h[:13], 16)
    prob = val_52 / (2 ** 52)
    if prob == 0:
        prob = 0.0000001

    multiplier = (100.0 - house_edge_pct) / (prob * 100.0)
    multiplier = max(1.00, round(multiplier, 2))

    if multiplier > 100.0:
        multiplier = round(1.00 + (int(h[:8], 16) % 9000) / 100.0, 2)

    return multiplier, h


st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("بيانات التحقق للجولة")
    server_seed = st.text_input("Server Seed (مشفر)", "green_gold_master_provably_fair_seed_2026")
    client_seed = st.text_input("Client Seed (عام)", "green_gold_client_seed_2026")
    nonce = st.number_input("Nonce (رقم المحاولة)", value=1, step=1, min_value=0)
    reported_multiplier = st.number_input("المضاعف المعلن", value=2.45, step=0.01, min_value=1.00)

with col2:
    st.subheader("نتيجة المطابقة والتدقيق")
    if st.button("🔍 إجراء التحقق الرياضي"):
        computed_mult, h = compute_multiplier(server_seed, client_seed, int(nonce))

        st.code(f"SHA-256 HMAC Hash: {h}")
        st.metric("المضاعف المحسوب رياضياً", f"{computed_mult:.2f}x")

        if abs(computed_mult - reported_multiplier) < 0.01:
            st.success("✅ النمط متطابق تماماً: الجولة نزيهة 100% ومثبتة تشفيرياً.")
        else:
            st.error(f"❌ عدم تطابق: المحسوب {computed_mult:.2f}x مقابل المعلن {reported_multiplier:.2f}x")

st.markdown("---")
st.markdown("### 🔬 الشرح العلمي")
st.markdown("تعتمد ألعاب كراش على تقنية **Provably Fair** حيث يتم تحديد نتيجة كل جولة قبل بدايتها وعرضها بـ Hash مشفر لا يمكن التلاعب به أثناء الطيران.")
