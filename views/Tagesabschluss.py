import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Tagesabschluss berechnen")

st.write("Bitte gebt die Daten für den Tagesabschluss ein.")

with st.form("tagesabschluss_formular"):
    name = st.text_input("Name")
    datum = st.date_input("Datum")

    startkasse = st.number_input("Startkasse (CHF)", min_value=0.0, step=1.0)
    bar_total = st.number_input("Bar-Einnahmen (CHF)", min_value=0.0, step=1.0)
    karte_total = st.number_input("Karten-Einnahmen (CHF)", min_value=0.0, step=1.0)
    twint_total = st.number_input("TWINT-Einnahmen (CHF)", min_value=0.0, step=1.0)

    soll_betrag = st.number_input("Soll-Betrag / erwarteter Umsatz (CHF)", min_value=0.0, step=1.0)

    berechnen = st.form_submit_button("Berechnen")

if berechnen:
    total = bar_total + karte_total + twint_total
    differenz = total - soll_betrag

    st.subheader("Ergebnis")
    st.write(f"**Name:** {name}")
    st.write(f"**Datum:** {datum}")
    st.write(f"**Total:** {total:.2f} CHF")
    st.write(f"**Differenz:** {differenz:.2f} CHF")

    if differenz > 0:
        st.success("Es wurde mehr eingenommen als erwartet.")
    elif differenz < 0:
        st.error("Es wurde weniger eingenommen als erwartet.")
    else:
        st.info("Der Betrag stimmt genau.")

    # Optional: schon fürs spätere Speichern vorbereiten
    neuer_eintrag = pd.DataFrame([{
        "timestamp": datetime.now(),
        "name": name,
        "datum": str(datum),
        "startkasse": startkasse,
        "bar_total": bar_total,
        "karte_total": karte_total,
        "twint_total": twint_total,
        "soll_betrag": soll_betrag,
        "total": total,
        "differenz": differenz
    }])

    st.write("Vorschau des Datensatzes:")
    st.dataframe(neuer_eintrag, use_container_width=True)