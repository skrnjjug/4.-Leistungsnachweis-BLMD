import streamlit as st
from utils.data_manager import get_data

st.title("📊 Übersicht")

df = get_data()

if df.empty:
    st.info("Noch keine Daten vorhanden.")
else:
    st.dataframe(df, use_container_width=True)