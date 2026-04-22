import streamlit as st

st.set_page_config(page_title="BarCalc", page_icon="🍸", layout="wide")

# STATE INIT
if "history" not in st.session_state:
    st.session_state.history = []

if "mitarbeiter" not in st.session_state:
    st.session_state.mitarbeiter = []

# UI
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

col1, col2 = st.columns(2)

with col1:
    if st.button("🔢 Neuer Tagesabschluss", use_container_width=True):
        st.session_state.mitarbeiter = []
        st.switch_page("pages/calculator.py")

with col2:
    if st.button("📊 Verlauf", use_container_width=True):
        st.switch_page("pages/verlauf.py")