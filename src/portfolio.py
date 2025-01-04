import streamlit as st
import os

st.title("💼 Portfolio", anchor=False)

if os.path.exists('trades.ddb'):
    st.write("placeholder")