import streamlit as st
import os
from helpers.database_helper import fetch_data

st.title("📊 Portfolio", anchor=False)

if os.path.exists('trades.ddb'):
    st.subheader("Opened Positions", anchor=False)
    opened_df = fetch_data("SELECT * FROM positions WHERE remaining > 0")
    st.dataframe(opened_df)

    st.subheader("Closed Positions", anchor=False)
    closed_df =  fetch_data("SELECT * FROM positions WHERE remaining = 0")
    st.dataframe(closed_df)