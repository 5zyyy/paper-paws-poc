import duckdb
import os
import streamlit as st

def create_db():
    """
    Create the database and tables if they do not exist.
    """
    with duckdb.connect('trades.ddb') as con:
        con.execute(f'''
            CREATE TABLE IF NOT EXISTS transactions (
                date DATE,
                time TIME,
                symbol TEXT,
                token TEXT,
                contract_address TEXT,
                action TEXT,
                market_cap REAL,
                token_price REAL,
                token_amt REAL,
                total REAL
            );
        ''')

        con.execute(f'''
            CREATE TABLE IF NOT EXISTS positions (
                date DATE,
                time TIME,
                symbol TEXT,
                token TEXT,
                contract_address TEXT,
                market_cap REAL,
                average_market_cap REAL,
                initial_investment REAL,
                remaining REAL,
                sold REAL,
                unrealized_profit REAL,
                realized_profit REAL,
                roi REAL,
                total_token_amt REAL,
                remaining_token_amt REAL
            );
        ''')

def delete_db():
    """
    Delete the database file.
    """
    os.remove('trades.ddb')

def insert_to_db(table, data):
    """
    Insert data into the specified table.

    Parameters:
    - table (str): The table to insert data into.
    - data (list): The data to insert.
    """
    with duckdb.connect('trades.ddb') as con:
        if table == 'transactions':
            query = f'''
                INSERT INTO {table} (date, time, symbol, token, contract_address, action, market_cap, token_price, token_amt, total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

        elif table == 'positions':
            query = f'''
                INSERT INTO {table} (date, time, symbol, token, contract_address, market_cap, average_market_cap, initial_investment, remaining, sold, unrealized_profit, realized_profit, roi, total_token_amt, remaining_token_amt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

        con.executemany(query, data)

def fetch_data(query):
    """
    Fetch data from the database using a SQL query.

    Parameters:
    - query (str): The SQL query to execute.

    Returns:
    - pd.DataFrame: The result of the query as a DataFrame.
    """
    with duckdb.connect('trades.ddb') as con:
        data = con.sql(query).df()
    return data

def fetch_data_paginated(query, page_number, total_rows, type):
    """
    Fetch paginated data from the database using a SQL query.

    Parameters:
    - query (str): The SQL query to execute.
    - page_number (int): The current page number.
    - total_rows (int): Total number of rows in the table.
    - type (str): The type of data to fetch.

    Returns:
    - pd.DataFrame or None: The paginated result of the query as a DataFrame
    - int or None: Total number of pages
    - Boolean: True if the page number is out of bounds, False otherwise
    """
    page_size = 20
    total_pages = (total_rows + page_size - 1) // page_size

    if type == 'trade_history':
        if st.session_state.trade_history_page_number > total_pages:
            st.session_state.trade_history_page_number = total_pages
            return None, None, True
        
        elif st.session_state.trade_history_page_number < 1:
            st.session_state.trade_history_page_number = 1
            return None, None, True
    elif type == 'closed_positions':
        if st.session_state.closed_positions_page_number > total_pages:
            st.session_state.closed_positions_page_number = total_pages
            return None, None, True
        
        elif st.session_state.closed_positions_page_number < 1:
            st.session_state.closed_positions_page_number = 1
            return None, None, True

    offset = (page_number - 1) * page_size
    query = f"{query} ORDER BY date DESC, time DESC LIMIT {page_size} OFFSET {offset}"
    df = fetch_data(query)
    return df, total_pages, False

def delete_position(contract_address):
    """
    Delete positions from the database based on contract address.

    Parameters:
    - contract_address (str or list): The contract address(es) to delete.
    """
    with duckdb.connect('trades.ddb') as con:
        contract_address_str = ""
        if isinstance(contract_address, list):
            for index, ca in enumerate(contract_address):
                contract_address_str += f"'{ca}'"
                if index != len(contract_address) - 1:
                    contract_address_str += ", "

        elif isinstance(contract_address, str):
            contract_address_str = f"'{contract_address}'"

        else:
            return "ERROR: contract_address is neither a list nor a string"
        
        con.execute(f"DELETE FROM positions WHERE contract_address IN ({contract_address_str})")
