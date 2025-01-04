from datetime import datetime
from helpers.settings_helper import SettingsConfiguration
from helpers.api_helper import QueryAPI
from helpers.database_helper import insert_to_db, fetch_data, delete_open_position

class SubmitOrder:
    def __init__(self):
        self.settings = SettingsConfiguration('settings.yaml')
        self.api_key = self.settings.get_settings()['api_key']
        self.query_api = QueryAPI(self.api_key)

    def calulcate_token_amt(self, total, token_price, sol_price):
        return (sol_price * total)/token_price
    
    def calculate_avg_mc(self, contract_address):
        df = fetch_data(f"SELECT * FROM transactions WHERE contract_address = '{contract_address}'")
        
        total_tokens = df['token_amt'].sum()
        
        weighted_mcs_list = []
        for index, row in df.iterrows():
            token_amt = row['token_amt']
            market_cap = row['market_cap']

            weighted_mc = token_amt * market_cap
            weighted_mcs_list.append(weighted_mc)
        
        weighted_mcs = sum(weighted_mcs_list)
        avg_mc = weighted_mcs/total_tokens

        return avg_mc
    
    def add_to_trade_history(self, contract_address, buy_amt):
        token_details  = self.query_api.get_details(contract_address)
        if isinstance(token_details, int):
            return token_details
        sol_price = self.query_api.get_details()

        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        symbol = token_details['symbol']
        name = token_details['name']
        mc = token_details['market_data']['market_cap']['usd']
        token_price = token_details['market_data']['current_price']['usd']
        token_amt = self.calulcate_token_amt(buy_amt, token_price, sol_price['solana']['usd'])

        data = (date, time, symbol, name, contract_address, 'buy', mc, token_price, token_amt, buy_amt)
        insert_to_db('transactions', data)
        return data

    def buy_coin(self, contract_address, buy_amt):
        if contract_address == '':
            return 998
        if buy_amt <= 0:
            return 999
        data = self.add_to_trade_history(contract_address, buy_amt)
        if isinstance(data, int):
            return data
        df = fetch_data(f"SELECT * FROM open_positions WHERE contract_address = '{contract_address}'")

        if not df.empty:
            date = data[0]
            time = data[1]
            avg_mc = float(self.calculate_avg_mc(contract_address))
            initial_investment = float(df['initial_investment'] + buy_amt)
            remaining = float(df['remaining'] + buy_amt)
            data = (date, time, df['symbol'].iloc[0], df['token'].iloc[0], df['contract_address'].iloc[0], avg_mc, initial_investment, remaining, float(df['sold'].iloc[0]))
            delete_open_position(contract_address)
            insert_to_db('open_positions', data)
        
        else:
            date = data[0]
            time = data[1]
            symbol = data[2]
            token = data[3]
            avg_mc = data[6]
            initial_investment = remaining = data[9]
            sold = 0
            data = (date, time, symbol, token, contract_address, avg_mc, initial_investment, remaining, sold)
            insert_to_db('open_positions', data)