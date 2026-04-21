import streamlit as st

# Titel
st.markdown(
    """
    <h1 style='text-align: center;'>BarCalc 🍸</h1>
    <p style='text-align: center; font-size: 18px;'>
    Eure smarte Tagesabschluss-App für die Bar
    </p>
    """,
    unsafe_allow_html=True
)

st.write("")

# Info-Box
st.markdown(
    """
    <div style="
        background-color:#f5f7fb;
        padding:20px;
        border-radius:12px;
        border:1px solid #d9e2f0;
    ">
    <h3>Willkommen 👋</h3>
    <p>
    Mit <b>BarCalc</b> könnt ihr euren täglichen Kassenabschluss schnell und einfach berechnen.
    </p>
    <p>
    Gebt eure Einnahmen ein, klickt auf <b>Berechnen</b> und erhaltet sofort euer Ergebnis.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# Features / Übersicht
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔢 Tagesabschluss")
    st.write("Berechne deinen Umsatz und die Differenz in Sekunden.")

with col2:
    st.markdown("### 📊 Übersicht")
    st.write("Behalte den Überblick über deine Einnahmen.")

st.write("")

# Hinweis
st.info("👉 Gehe zur Seite **'Tagesabschluss'**, um deinen Abschluss zu berechnen.")