import streamlit as st
from helpers.database_helper import fetch_data

st.title("🗓️ Trade History", anchor=False)

df = fetch_data("SELECT * FROM transactions")
st.dataframe(df)