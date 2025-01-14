import yaml
import pandas as pd

def write_yaml(path, content):
    with open(path, 'w') as file:
        yaml.dump(content, file)

def format_number(value):
    if pd.isna(value):
        return value
    
    abs_value = abs(value)
    if value < 0:
        sign = '-'
    else:
        sign = ''
    
    if abs_value >= 1_000_000_000:
        return f"{sign}{abs_value/1_000_000_000:.2f}b"
    elif abs_value >= 1_000_000:
        return f"{sign}{abs_value/1_000_000:.2f}m"
    elif abs_value >= 1_000:
        return f"{sign}{abs_value/1_000:.2f}k"
    else:
        return f"{sign}{abs_value:.2f}"

def format_positions_df(df):
    df = df.drop(['total_token_amt', 'remaining_token_amt'], axis=1)
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    columns_to_format = ['market_cap', 'average_market_cap']
    
    for col in columns_to_format:
        df[col] = df[col].apply(format_number)
    
    df['roi'] = df['roi'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else x)
    
    df = df.rename(columns={
        'date': 'Date',
        'time': 'Time', 
        'symbol': 'Symbol',
        'token': 'Token Name',
        'contract_address': 'Contract Address',
        'market_cap': 'Market Cap',
        'average_market_cap': 'Avg Market Cap',
        'initial_investment': 'Initial Investment (SOL)',
        'remaining': 'Remaining Value (SOL)',
        'sold': 'Sold Amount (SOL)',
        'unrealized_profit': 'Unrealized P/L (SOL)',
        'realized_profit': 'Realized P/L (SOL)',
        'roi': 'ROI %'
    })

    return df

def format_transactions_df(df):
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    columns_to_format = ['market_cap', 'token_amt']
    
    for col in columns_to_format:
        df[col] = df[col].apply(format_number)
    
    df = df.rename(columns={
        'date': 'Date',
        'time': 'Time', 
        'symbol': 'Symbol',
        'token': 'Token Name',
        'contract_address': 'Contract Address',
        'action': 'Action',
        'market_cap': 'Market Cap',
        'token_price': 'Token Price (USD)',
        'token_amt': 'Token Amount',
        'total': 'Total (SOL)'
    })
    
    return df