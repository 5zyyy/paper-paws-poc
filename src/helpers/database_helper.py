import duckdb
import os

def create_db():
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
            CREATE TABLE IF NOT EXISTS open_positions (
                date DATE,
                time TIME,
                symbol TEXT,
                token TEXT,
                contract_address TEXT,
                average_market_cap REAL,
                initial_investment REAL,
                remaining REAL,
                sold REAL
            );
        ''')

def delete_db():
    os.remove('trades.ddb')

def insert_to_db(table, data):
    with duckdb.connect('trades.ddb') as con:
        if table == 'transactions':
            query = f'''
                INSERT INTO {table} (date, time, symbol, token, contract_address, action, market_cap, token_price, token_amt, total)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            '''

        elif table == 'open_positions':
            query = f'''
                INSERT INTO {table} (date, time, symbol, token, contract_address, average_market_cap, initial_investment, remaining, sold)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            '''

        con.execute(query, data)

def fetch_data(query):
    with duckdb.connect('trades.ddb') as con:
        data = con.sql(query).df()
    return data

def delete_open_position(contract_address):
    with duckdb.connect('trades.ddb') as con:
        con.execute(f"DELETE FROM open_positions WHERE contract_address = '{contract_address}'")