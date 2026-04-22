import streamlit as st
import pandas as pd

st.markdown("## 📊 Verlauf")

st.caption("Hier siehst du alle gespeicherten Tagesabschlüsse.")

# Falls data_df noch nicht im session state vorhanden ist, Daten laden
if "data_df" not in st.session_state:
    data_manager = st.session_state["data_manager"]
    st.session_state["data_df"] = data_manager.load_user_data(
        "data.csv",
        initial_value=pd.DataFrame(),
        parse_dates=["timestamp"]
    )

data_df = st.session_state["data_df"]

if data_df.empty:
    st.info("Noch keine gespeicherten Einträge vorhanden.")
else:
    st.markdown("### Gespeicherte Tagesabschlüsse")
    st.dataframe(data_df, use_container_width=True)

    # Optional: wichtigste Kennzahlen oben anzeigen
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Einträge", len(data_df))

    with col2:
        st.metric("Gesamteinnahmen", f"{data_df['total'].sum():.2f} CHF")

    with col3:
        if "trinkgeld_total" in data_df.columns:
            st.metric("Gesamtes Trinkgeld", f"{data_df['trinkgeld_total'].sum():.2f} CHF")

st.markdown("---")

if st.button("🔙 Zurück zur Startseite", use_container_width=True):
    st.switch_page("views/home.py")