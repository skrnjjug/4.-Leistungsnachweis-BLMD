import streamlit as st
from utils.data_manager import load_data

st.set_page_config(
    page_title="Startseite | BarCalc",
    page_icon="🍸",
    layout="wide"
)

# =========================
# 🧠 STATE INIT
# =========================
if "history" not in st.session_state:
    st.session_state.history = load_data()

if "mitarbeiter" not in st.session_state:
    st.session_state.mitarbeiter = []

# =========================
# 🎨 STYLE
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    background: #f8fafc;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    text-align: center;
    height: 150px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 10px;
    color: #1f2937;
}

.card-sub {
    font-size: 14px;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🏠 HEADER
# =========================
st.markdown("""
<div style="
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
">
    <h1>🍸 BarCalc</h1>
    <p>Kassenabschluss einfach gemacht</p>
</div>
""", unsafe_allow_html=True)

# =========================
# NAVIGATION
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div style="font-size:30px;">🔢</div>
        <div class="card-title">Tagesabschluss</div>
        <div class="card-sub">Neuen Abschluss berechnen</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Starten", use_container_width=True):
        st.session_state.mitarbeiter = []
        st.switch_page("pages/calculator.py")


with col2:
    st.markdown("""
    <div class="card">
        <div style="font-size:30px;">📊</div>
        <div class="card-title">Verlauf</div>
        <div class="card-sub">Vergangene Daten ansehen</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Öffnen", use_container_width=True):
        st.switch_page("pages/verlauf.py")