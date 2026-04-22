import pandas as pd
import streamlit as st

def init_data():
    if "data" not in st.session_state:
        st.session_state["data"] = pd.DataFrame()

def add_entry(entry_df):
    init_data()
    st.session_state["data"] = pd.concat(
        [st.session_state["data"], entry_df],
        ignore_index=True
    )

def get_data():
    init_data()
    return st.session_state["data"]