import streamlit as st
import time
from streamlit_extras.stylable_container import stylable_container
import os
from helpers.settings_helper import SettingsConfiguration, reset_db_confirmation, delete_db_confirmation
from helpers.database_helper import create_db

settings = SettingsConfiguration('settings.yaml')
settings_data = settings.get_settings()

st.title("⚙️ Settings")
with st.container(border=True):
    if settings_data['api_key'] == '':
        api_key_text = 'None'
    else:
        api_key_text = settings_data['api_key']

    st.subheader(f"Balance: {settings_data['balance']} sol", anchor=False)
    with st.popover('Edit'):
        with st.form('balance_edit', border=False):
            new_balance = st.number_input('Edit balance')
            submitted = st.form_submit_button("Submit")
            if submitted:
                settings.update_settings('balance', new_balance)

    st.subheader(f"Buy Fee: {settings_data['buy_fee']} sol", anchor=False)
    with st.popover('Edit'):
        with st.form('buyfee_edit', border=False):
            new_buyfee = st.number_input('Edit buy fee')
            submitted = st.form_submit_button("Submit")
            if submitted:
                settings.update_settings('buy_fee', new_buyfee)

    st.subheader(f"Sell Fee: {settings_data['sell_fee']} sol", anchor=False)
    with st.popover('Edit'):
        with st.form('sellfee_edit', border=False):
            new_sellfee = st.number_input('Edit sell fee')
            submitted = st.form_submit_button("Submit")
            if submitted:
                settings.update_settings('sell_fee', new_sellfee)

    st.subheader(f"Coin Gecko API Key:", anchor=False)
    st.code(api_key_text, language="plaintext")
    with st.popover('Edit'):
        with st.form('apikey_edit', border=False):
            new_apikey = st.text_input('Edit api key')
            submitted = st.form_submit_button("Submit")
            if submitted:
                settings.update_settings('api_key', new_apikey)

    st.subheader("Database", anchor=False)
    if os.path.exists('trades.ddb'):
        
        with stylable_container(
            key='reset_del_btn_container',
            css_styles="""
            {
                width: 154px;
            }
            """
        ):
            col1, col2 = st.columns([1, 1])

            with col1:
                reset_btn = st.button("Reset", type="primary")
                if reset_btn:
                    reset_db_confirmation()

            with col2:
                delete_btn = st.button("Delete", type="primary")
                if delete_btn:
                    delete_db_confirmation()
    else:
        create_btn = st.button("Create")
        if create_btn:
            create_db()
            st.toast("Database Created!", icon='💾')
            time.sleep(1)
            st.rerun()

    st.subheader("Version: 1.0.0", anchor=False)
    check_update_btn = st.button("Check for updates")

st.write(
    "Made by [awl](https://github.com/5zyyy)",
    unsafe_allow_html=True
)