from helpers.database_helper import insert_to_db
from datetime import date, time

# Sample data for one row
transaction_row = [
    date(2024, 1, 1),           # date
    time(12, 0),                # time
    'SOL/USD',                  # symbol
    'BONK',                     # token
    '0x123456789',             # contract_address
    'BUY',                      # action
    1000000,                    # market_cap
    0.00001,                    # token_price
    1000000,                    # token_amt
    10                          # total
]

#closed positions only
position_row = [
    date(2024, 1, 1),           # date
    time(12, 0),                # time
    'SOL/USD',                  # symbol
    'BONK',                     # token
    '0x123456789',             # contract_address
    1000000,                    # market_cap
    1000000,                    # average_market_cap
    10,                         # initial_investment
    0,                          # remaining
    5,                          # sold
    2,                          # unrealized_profit
    2,                          # realized_profit
    40,                         # roi
    1000000,                    # total_token_amt
    500000                      # remaining_token_amt
]

# Create 100 copies of the sample data
transaction_data = [transaction_row for _ in range(100)]
position_data = [position_row for _ in range(100)]

# Insert the data
insert_to_db('transactions', transaction_data)
insert_to_db('positions', position_data)

print("Inserted 100 rows into both tables!")