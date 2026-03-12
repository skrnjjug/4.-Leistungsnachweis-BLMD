import pandas as pd 
import streamlit as st
from utils.data_manager import DataManager  # --- NEW CODE: import data manager ---

# Import the function to calculate the BMI
from functions.bmi_calculator import calculate_bmi

st.title('BMI Rechner')

with st.form("BMI Eingabeformular"):
    # Get user input for height and weight
    height = st.number_input('Geben Sie Ihre Größe ein (in Meter)', min_value=0.1, max_value=3.0, value=1.7, step=0.01)
    weight = st.number_input('Geben Sie Ihr Gewicht ein (in kg)', min_value=1.0, max_value=500.0, value=70.0, step=0.1)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    
if submitted:
    
    result = calculate_bmi(height, weight)
    
    st.write(f'Ihr BMI ist: {result["bmi"]}')
    st.write(f'Berechnet am: {result["timestamp"].strftime("%d.%m.%Y %H:%M:%S")}')
    st.write(f'Kategorie: {result["category"]}')

    st.session_state['data_df'] = pd.concat([st.session_state['data_df'], pd.DataFrame([result])])

    # --- CODE UPDATE: save data to data manager ---
    data_manager = DataManager()
    data_manager.save_user_data(st.session_state['data_df'], 'data.csv')
    # --- END OF CODE UPDATE ---
        
# display the data frame in a table
st.dataframe(st.session_state['data_df'])

