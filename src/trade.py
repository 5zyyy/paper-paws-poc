import streamlit as st
import os
import time
from helpers.database_helper import fetch_data
from helpers.trades_helper import SubmitOrder, get_open_token_contract
from helpers.settings_helper import SettingsConfiguration
from helpers.helpers import format_positions_df
from streamlit_extras.stylable_container import stylable_container

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
            ca_input_buy = st.text_input("Contract Address (CA)")
            buy_sol_amt = st.number_input("Buy Amount (sol)", min_value=0.0)
            submit_buy = st.button("BUY", use_container_width=True)
            if submit_buy:
                error = order.buy_coin(ca_input_buy, buy_sol_amt)
                if error is not None:
                    st.toast(f"{error}", icon='🚨')
                else:
                    st.toast(f"Buy order submitted! Priority fee: {priority_buy_fee}", icon='✅')
                    time.sleep(1)
                    st.rerun()

    with col2:
        options = get_open_token_contract()
        with st.container(border=True):
            st.header("Sell", anchor=False, divider='red')
            ca_input_sell = st.selectbox("Select token", options)
            sell_percentage_radio = st.radio(
                "Sell percentage",
                [None, "25%", "50%", "75%", "100%"],
                horizontal=True
            )
            if sell_percentage_radio is None:
                st.session_state['disable_number_input'] = False
            else:
                st.session_state['disable_number_input'] = True
            sell_percentage_input = st.number_input("Sell percentage", min_value=0.0, max_value=100.0, label_visibility='collapsed', disabled=st.session_state['disable_number_input'])
            submit_sell = st.button("SELL", type='primary', use_container_width=True)
            if submit_sell:
                if st.session_state['disable_number_input']:
                    sell_percentage = sell_percentage_radio
                else:
                    sell_percentage = sell_percentage_input
                error = order.sell_coin(ca_input_sell, sell_percentage)
                if error is not None:
                    st.toast(f"{error}", icon='🚨')
                else:
                    st.toast(f"Sell order submitted! Priority fee: {priority_buy_fee}", icon='✅')
                    time.sleep(1)
                    st.rerun()

    st.header("🟢 Positions", anchor=False)
    with stylable_container(
        key="refresh_button",
        css_styles="""
            {
                position: relative;
                width: 10px;
                margin-top: -53px;
                margin-left: 200px;
            }
            .st-key-refresh_btn button {
                background-color: transparent !important;
                border: none !important;
                padding: 2px 15px !important;
                transition: all 0.2s ease;
                color: rgba(255, 255, 255, 0.7) !important;
                font-size: 20px !important;
            }
            .st-key-refresh_btn button:hover {
                color: rgba(255, 255, 255, 1) !important;
                transform: rotate(180deg) scale(1.3);
            }
        """
    ):
        with st.container(key="refresh_btn"):
            refresh_open_positions = st.button("↻", help="Refresh")

    if refresh_open_positions:
        error = order.refresh_token()
        if error is None:
            refresh_toast_text = "Opened positions refreshed!"
        else:
            refresh_toast_text = error
        st.toast(refresh_toast_text, icon='🔄')

    df = fetch_data("SELECT * FROM positions WHERE remaining > 0 ORDER BY date DESC, time DESC")
    if df.empty:
        st.info("No opened positions found")
    else:
        st.dataframe(format_positions_df(df), hide_index=True)