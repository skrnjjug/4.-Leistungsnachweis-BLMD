import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Tagesabschluss")
st.caption("Erfasse die Einnahmen des Tages und berechne den Abschluss.")

st.markdown(
    """
    <style>
    .result-box {
        padding: 1rem;
        border-radius: 12px;
        background-color: #f5f7fb;
        border: 1px solid #d9e2f0;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .result-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.form("tagesabschluss_formular"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        datum = st.date_input("Datum")
        startkasse = st.number_input("Startkasse (CHF)", min_value=0.0, step=1.0)

    with col2:
        soll_betrag = st.number_input("Soll-Betrag / erwarteter Umsatz (CHF)", min_value=0.0, step=1.0)
        trinkgeld = st.number_input("Trinkgeld (CHF)", min_value=0.0, step=1.0)

    st.markdown("### Einnahmen")

    col3, col4, col5 = st.columns(3)

    with col3:
        bar_total = st.number_input("Bar-Einnahmen (CHF)", min_value=0.0, step=1.0)

    with col4:
        karte_total = st.number_input("Karten-Einnahmen (CHF)", min_value=0.0, step=1.0)

    with col5:
        twint_total = st.number_input("TWINT-Einnahmen (CHF)", min_value=0.0, step=1.0)

    berechnen = st.form_submit_button("Berechnen")

if berechnen:
    if not name:
        st.error("Bitte gib einen Namen ein.")
        st.stop()

    total = bar_total + karte_total + twint_total
    differenz = total - soll_betrag

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown('<div class="result-title">Ergebnis</div>', unsafe_allow_html=True)

    erg_col1, erg_col2 = st.columns(2)

    with erg_col1:
        st.write(f"**Name:** {name}")
        st.write(f"**Datum:** {datum}")
        st.write(f"**Startkasse:** {startkasse:.2f} CHF")
        st.write(f"**Trinkgeld:** {trinkgeld:.2f} CHF")

    with erg_col2:
        st.write(f"**Total Einnahmen:** {total:.2f} CHF")
        st.write(f"**Soll-Betrag:** {soll_betrag:.2f} CHF")
        st.write(f"**Differenz:** {differenz:.2f} CHF")

    st.markdown("</div>", unsafe_allow_html=True)

    if differenz > 0:
        st.success("Es wurde mehr eingenommen als erwartet.")
    elif differenz < 0:
        st.error("Es wurde weniger eingenommen als erwartet.")
    else:
        st.info("Der Betrag stimmt genau.")

    neuer_eintrag = pd.DataFrame([{
        "timestamp": datetime.now(),
        "name": name,
        "datum": str(datum),
        "startkasse": startkasse,
        "bar_total": bar_total,
        "karte_total": karte_total,
        "twint_total": twint_total,
        "trinkgeld": trinkgeld,
        "soll_betrag": soll_betrag,
        "total": total,
        "differenz": differenz
    }])

    st.markdown("### Vorschau des Datensatzes")
    st.dataframe(neuer_eintrag, use_container_width=True)

    if "data_df" in st.session_state:
        st.session_state["data_df"] = pd.concat(
            [st.session_state["data_df"], neuer_eintrag],
            ignore_index=True
        )
        st.success("Eintrag wurde zur aktuellen Session hinzugefügt.")