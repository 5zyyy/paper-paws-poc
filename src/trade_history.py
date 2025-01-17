import streamlit as st
import os
from helpers.database_helper import fetch_data, fetch_data_paginated
from helpers.helpers import format_transactions_df, convert_df

st.title("🗓️ Trade History", anchor=False)

if os.path.exists('trades.ddb'):
    total_rows = fetch_data("SELECT COUNT(*) as count FROM transactions").iloc[0]['count']

    if total_rows == 0:
        st.info("No trade history found")
    else:
        if st.button("Download"):
            st.toast("📥 Downloading trade history...")
            df = fetch_data("SELECT * FROM transactions ORDER BY date DESC, time DESC")
            df = format_transactions_df(df)
            csv = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📄 Click to save file",
                data=csv,
                file_name="trade_history.csv",
                mime="text/csv"
            )


        if 'trade_history_page_number' not in st.session_state:
            st.session_state.trade_history_page_number = 1

        df, total_pages, error = fetch_data_paginated(
            "SELECT * FROM transactions", 
            st.session_state.trade_history_page_number, 
            total_rows,
            'trade_history'
        )
        
        if df is not None:
            st.dataframe(format_transactions_df(df), hide_index=True)
        
        if error:
            st.rerun()
        else:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("⬅️ Previous", disabled=(st.session_state.trade_history_page_number == 1)):
                    st.session_state.trade_history_page_number -= 1
                    st.rerun()
                with col2:
                    st.write(f"Page {st.session_state.trade_history_page_number} of {total_pages}")
                with col3:
                    if st.button("Next ➡️", disabled=(st.session_state.trade_history_page_number == total_pages)):
                        st.session_state.trade_history_page_number += 1
                        st.rerun()