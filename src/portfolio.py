import streamlit as st
import os
from helpers.database_helper import fetch_data, fetch_data_paginated
import pandas as pd
from helpers.helpers import format_positions_df

st.title("📊 Portfolio", anchor=False)

if os.path.exists('trades.ddb'):
    # Fetch all positions data
    all_positions = fetch_data("SELECT * FROM positions")
    
    # Calculate portfolio summary metrics
    if not all_positions.empty:
        total_invested = all_positions['initial_investment'].sum()
        total_realized = all_positions['realized_profit'].sum()
        total_unrealized = all_positions['unrealized_profit'].sum()
        total_value = all_positions['remaining'].sum() + all_positions['sold'].sum()
        
        # Calculate overall ROI
        overall_roi = ((total_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
        
        # Create portfolio summary section
        st.subheader("Portfolio Summary", anchor=False)
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Invested", f"{total_invested:.3f} SOL")
                st.metric("Total Current Value", f"{total_value:.3f} SOL")
                
            with col2:
                st.metric("Realized P/L", f"{total_realized:.3f} SOL",
                         delta=f"{total_realized/total_invested*100:.1f}%" if total_invested > 0 else "0%")
                st.metric("Unrealized P/L", f"{total_unrealized:.3f} SOL",
                         delta=f"{total_unrealized/total_invested*100:.1f}%" if total_invested > 0 else "0%")
                
            with col3:
                st.metric("Total P/L", f"{(total_realized + total_unrealized):.3f} SOL")
                st.metric("Overall ROI", f"{overall_roi:.1f}%")

    # Display positions
    st.subheader("Opened Positions", anchor=False)
    opened_df = fetch_data("SELECT * FROM positions WHERE remaining > 0")
    if opened_df.empty:
        st.info("No opened positions found")
    else:
        st.dataframe(format_positions_df(opened_df), hide_index=True)

    st.subheader("Closed Positions", anchor=False)
    total_closed = fetch_data("SELECT COUNT(*) as count FROM positions WHERE remaining = 0").iloc[0]['count']
    
    if total_closed == 0:
        st.info("No closed positions found")
    else:
        if 'closed_positions_page_number' not in st.session_state:
            st.session_state.closed_positions_page_number = 1

        df, total_pages, error = fetch_data_paginated(
            "SELECT * FROM positions WHERE remaining = 0", 
            st.session_state.closed_positions_page_number, 
            total_closed,
            'closed_positions'
        )
        
        if df is not None:
            st.dataframe(format_positions_df(df), hide_index=True)
        
        if error:
            st.rerun()
        else:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("⬅️ Previous", disabled=(st.session_state.closed_positions_page_number == 1)):
                    st.session_state.closed_positions_page_number -= 1
                    st.rerun()
            with col2:
                st.write(f"Page {st.session_state.closed_positions_page_number} of {total_pages}")
            with col3:
                if st.button("Next ➡️", disabled=(st.session_state.closed_positions_page_number == total_pages)):
                    st.session_state.closed_positions_page_number += 1
                    st.rerun()