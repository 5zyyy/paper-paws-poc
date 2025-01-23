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
    os.remove('trades.ddb')

def insert_to_db(table, data):
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
    with duckdb.connect('trades.ddb') as con:
        data = con.sql(query).df()
    return data

def delete_position(contract_address):
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
