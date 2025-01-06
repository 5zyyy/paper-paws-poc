import streamlit as st
import os
from helpers.database_helper import fetch_data

st.title("📊 Portfolio", anchor=False)

if os.path.exists('trades.ddb'):
    df = fetch_data("SELECT * FROM WHERE remaining = 0")
    st.dataframe(df)