import streamlit as st
import os
from helpers.database_helper import fetch_data

st.title("🗓️ Trade History", anchor=False)

if os.path.exists('trades.ddb'):
    df = fetch_data("SELECT * FROM transactions")
    st.dataframe(df)