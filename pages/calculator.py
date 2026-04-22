import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import add_entry

st.title("🔢 Tagesabschluss")

with st.form("abschluss"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        datum = st.date_input("Datum")
        startkasse = st.number_input("Startkasse", 0.0)

    with col2:
        soll = st.number_input("Soll-Betrag", 0.0)
        trinkgeld = st.number_input("Trinkgeld", 0.0)

    st.subheader("Einnahmen")
    bar = st.number_input("Bar", 0.0)
    karte = st.number_input("Karte", 0.0)
    twint = st.number_input("TWINT", 0.0)

    submit = st.form_submit_button("Berechnen")

if submit:
    total = bar + karte + twint
    diff = total - soll

    st.success(f"Total: {total:.2f} CHF")
    st.write(f"Differenz: {diff:.2f} CHF")

    df = pd.DataFrame([{
        "timestamp": datetime.now(),
        "name": name,
        "datum": datum,
        "startkasse": startkasse,
        "bar": bar,
        "karte": karte,
        "twint": twint,
        "trinkgeld": trinkgeld,
        "soll": soll,
        "total": total,
        "diff": diff
    }])

    add_entry(df)
    st.success("Gespeichert!")