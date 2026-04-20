import pandas as pd
import streamlit as st

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

st.set_page_config(
    page_title="BarCalc",
    page_icon=":material/calculate:"
)

data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="app_data"
)

login_manager = LoginManager(data_manager)
login_manager.login_register()

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame(),
        parse_dates=['timestamp']
    )

pg_home = st.Page(
    "views/home.py",
    title="Home",
    icon=":material/home:",
    default=True
)

pg_calc = st.Page(
    "views/calculator.py",
    title="Tagesabschluss",
    icon=":material/calculate:"
)

pg = st.navigation([pg_home, pg_calc])
pg.run()
