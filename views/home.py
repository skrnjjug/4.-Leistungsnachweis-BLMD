import streamlit as st

# --- HERO SECTION ---
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        color: white;
    ">
        <h1>BarCalc 🍸</h1>
        <p style="font-size:18px;">
        Dein smarter Begleiter für den täglichen Kassenabschluss
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# --- FEATURES / NAVIGATION ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="
            background-color:#111827;
            padding:20px;
            border-radius:12px;
            border:1px solid #2d3748;
        ">
            <h3>🔢 Tagesabschluss</h3>
            <p>Berechne deinen Umsatz und die Differenz in Sekunden.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("➡️ Zum Rechner"):
        st.switch_page("views/calculator.py")


with col2:
    st.markdown(
        """
        <div style="
            background-color:#111827;
            padding:20px;
            border-radius:12px;
            border:1px solid #2d3748;
        ">
            <h3>📊 Übersicht</h3>
            <p>Behalte den Überblick über deine Einnahmen.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button("📈 Bald verfügbar", disabled=True)

st.write("")

# --- EXTRA NICE TOUCH ---
st.markdown("---")
st.caption("💡 Tipp: Starte direkt mit dem Tagesabschluss und teste deine App.")