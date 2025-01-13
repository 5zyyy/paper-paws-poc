import streamlit as st
import os
from helpers.database_helper import fetch_data

st.title("🗓️ Trade History", anchor=False)

if os.path.exists('trades.ddb'):
    df = fetch_data("SELECT * FROM transactions")
    if df.empty:
        st.info("No trade history found")
    else:
        st.dataframe(df)