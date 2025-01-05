import streamlit as st
import os
import time
from helpers.database_helper import fetch_data
from helpers.trades_helper import SubmitOrder, get_open_token_contract
from helpers.settings_helper import SettingsConfiguration

st.title("📈 Trade", anchor=False)

settings = SettingsConfiguration('settings.yaml')
priority_buy_fee = settings.get_settings()['priority_buy_fee']
priority_sell_fee = settings.get_settings()['priority_sell_fee']

if os.path.exists('trades.ddb'):
    order = SubmitOrder()

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.container(border=True):
            st.header("Buy", anchor=False, divider='green')
            ca_input = st.text_input("Contract Address (CA)")
            buy_sol_amt = st.number_input("Buy Amount (sol)", min_value=0.0)
            submit_buy = st.button("BUY", use_container_width=True)
            if submit_buy:
                error = order.buy_coin(ca_input, buy_sol_amt)
                if error is not None:
                    st.toast(f"{error}", icon='🚨')
                else:
                    st.toast(f"Buy order submitted! Priority fee: {priority_buy_fee}", icon='✅')

    with col2:
        options = get_open_token_contract()
        with st.container(border=True):
            st.header("Sell", anchor=False, divider='red')
            st.selectbox("Select token", options)
            sell_percentage = st.radio(
                "Sell percentage",
                [None, "25%", "50%", "75%", "100%"],
                horizontal=True
            )
            if sell_percentage is None:
                st.session_state['disable_number_input'] = False
            else:
                st.session_state['disable_number_input'] = True
            st.number_input("Sell percentage", min_value=0.0, max_value=100.0, label_visibility='collapsed', disabled=st.session_state['disable_number_input'])
            submit_sell = st.button("SELL", type='primary', use_container_width=True)

    st.header("🟢 Positions", anchor=False)
    refresh_open_positions = st.button("🔄")
    if refresh_open_positions:
        error = order.refresh_token()
        if error is None:
            refresh_toast_text = "Opened positions refreshed!"
        else:
            refresh_toast_text = error
        st.toast(refresh_toast_text, icon='🔄')

    df = fetch_data("SELECT * FROM open_positions")
    st.dataframe(df)