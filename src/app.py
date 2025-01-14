import streamlit as st
import os
from helpers.helpers import write_yaml
from helpers.settings_helper import SettingsConfiguration

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        [data-testid="stBaseButton-headerNoPadding"],
        [data-testid="stBaseButton-header"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

if not os.path.exists('trades.ddb'):
    st.error('Database does not exist! To start paper trading, create a database in settings.', icon="🚨")

settings_file = 'settings.yaml'
settings = {
    'balance': 3,
    'priority_buy_fee': 0.01,
    'priority_sell_fee': 0.01,
    'api_key': ''
}

if not os.path.exists(settings_file):
    st.toast("Creating settings file...", icon='⚙️')
    write_yaml(settings_file, settings)
    st.toast("Settings file created!", icon='✅')

settings = SettingsConfiguration('settings.yaml')
balance = settings.get_settings()['balance']

with st.sidebar:
    st.title("💰 Balance")
    st.code(f"{balance:.3f} sol")
    st.title("🐾 Paper Paws POC", anchor=False)
    st.write("Version: 1.0.0")
    st.write(
        "Made by [awl](https://x.com/5zy12), [ryan](https://x.com), [mark](https://x.com)",
        unsafe_allow_html=True
    )

pg = st.navigation([
    st.Page('trade.py', title="📈 Trade"), 
    st.Page('portfolio.py', title="📊 Portfolio"), 
    st.Page('trade_history.py', title="🗓️ Trade History"), 
    st.Page('settings.py', title="⚙️ Settings")
])
pg.run()