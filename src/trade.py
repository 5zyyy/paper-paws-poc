import streamlit as st
import os
import time
from helpers.database_helper import fetch_data
from helpers.trades_helper import SubmitOrder

st.title("📈 Trade", anchor=False)

if os.path.exists('trades.ddb'):
    order = SubmitOrder()

    options = ("Retard", "Autism") #mock options

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.form('buy_form'):
            st.header("Buy", anchor=False, divider='green')
            ca_input = st.text_input("Contract Address (CA)")
            buy_sol_amt = st.number_input("Buy Amount (sol)", min_value=0)
            submit_buy = st.form_submit_button("BUY")
            if submit_buy:
                error = order.buy_coin(ca_input, buy_sol_amt)
                if error is not None:
                    # if error == 998:
                    #     error_msg = 'No contract address entered!'
                    # elif error == 999:
                    #     error_msg = 'Buy amount must be more than 0 sol!'
                    # elif error == 401 or error == 10002:
                    #     error_msg = f"API key missing or invalid (Status Code: {error})"
                    # elif error == 429:
                    #     error_msg = f"Too many requests! Please try again later (Status Code: {error})"
                    # elif error == 404:
                    #     error_msg = f"Coin not found! Check the CA (Status Code: {error})"
                    # else:
                    #     error_msg = f"Error encountered! (Status Code: {error})"
                    st.toast(f"{error}", icon='🚨')
                else:
                    st.toast("Buy order submitted!", icon='✅')
                    time.sleep(1)
                    st.rerun()

    with col2:
        with st.form('sell_form'):
            st.header("Sell", anchor=False, divider='red')
            st.selectbox("Select token", options)
            sell_percentage = st.radio(
                "Sell percentage",
                ["25%", "50%", "75%", "100%"],
                horizontal=True
            )
            submit_sell = st.form_submit_button("SELL", type='primary')

    st.header("🟢 Positions", anchor=False)
    df = fetch_data("SELECT * FROM open_positions")
    st.dataframe(df)