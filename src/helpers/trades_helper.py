from datetime import datetime
import streamlit as st
from helpers.settings_helper import SettingsConfiguration
from helpers.api_helper import QueryAPI
from helpers.database_helper import insert_to_db, fetch_data, delete_open_position

def get_open_token_contract():
    df = fetch_data("SELECT * FROM positions")
    token_contract_tuple = tuple(f"{token} - {contract}" for token, contract in zip(df['token'], df['contract_address']))
    return token_contract_tuple

class SubmitOrder:
    def __init__(self):
        self.settings = SettingsConfiguration('settings.yaml')
        self.settings_data = self.settings.get_settings()
        self.api_key = self.settings_data['api_key']
        self.balance = self.settings_data['balance']
        self.priority_buy_fee = self.settings_data['priority_buy_fee']
        self.priority_sell_fee = self.settings_data['priority_sell_fee']
        self.query_api = QueryAPI(self.api_key)

    def calulcate_token_amt(self, total, token_price, sol_price):
        return (sol_price * total)/token_price
    
    def calculate_avg_mc(self, contract_address):
        df = fetch_data(f"SELECT * FROM transactions WHERE contract_address = '{contract_address}' AND action = 'buy'")
        
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
    
    def calculate_changes(self, mc, amc, initial_not_sold):
        percentage_change = (mc - amc)/amc
        sol_difference = initial_not_sold * percentage_change
        return sol_difference

    def calculate_roi(self, initial_investment, remaining, sold):
        roi_percentage = (((remaining + sold) - initial_investment)/initial_investment) * 100
        return roi_percentage
    
    def add_to_trade_history(self, contract_address, amt, action):
        token_details = self.query_api.token_data(contract_address)
        if isinstance(token_details, str):
            return token_details
        sol_price = self.query_api.get_sol_price()
        if isinstance(sol_price, str):
            return sol_price

        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        symbol = token_details['symbol']
        name = token_details['name']
        mc = token_details['market_cap']
        token_price = token_details['token_price']
        token_amt = self.calulcate_token_amt(amt, token_price, sol_price['solana']['usd'])

        data =[[date, time, symbol, name, contract_address, action, mc, token_price, token_amt, amt]]
        insert_to_db('transactions', data)  
        return data
    
    def refresh_token(self):
        df = fetch_data("SELECT date, time, symbol, token, contract_address, average_market_cap, initial_investment, remaining, sold FROM positions")
        if df.empty:
            return "No open positions to refresh!"

        ca_to_refresh = []
        for ca in df['contract_address']:
            ca_to_refresh.append(ca)

        all_token_details = self.query_api.get_multiple_token_data(ca_to_refresh)

        to_insert = []
        for _, row in df.iterrows():
            ca = row['contract_address']
            mc = all_token_details[ca]['market_cap']
            initial_not_sold = row['initial_investment'] - row['sold']
            unrealized_profit = self.calculate_changes(mc, row['average_market_cap'], initial_not_sold)
            remaining = initial_not_sold + unrealized_profit
            roi = self.calculate_roi(row['initial_investment'], remaining, row['sold'])
            data = [row['date'], row['time'], row['symbol'], row['token'], row['contract_address'], mc, row['average_market_cap'], row['initial_investment'], remaining, row['sold'], unrealized_profit, roi]
            to_insert.append(data)

        delete_open_position(ca_to_refresh)
        insert_to_db('positions', to_insert)

    def buy_coin(self, contract_address, buy_amt):
        if contract_address == '':
            return 'No contract address entered!'
        if buy_amt <= 0:
            return 'Buy amount must be more than 0 sol!'
        if self.balance - buy_amt < 0:
            return 'Insufficient balance!'
        actual_buy_amt = buy_amt - self.priority_buy_fee
        data = self.add_to_trade_history(contract_address, actual_buy_amt, 'buy')
        if isinstance(data, str):
            return data
        df = fetch_data(f"SELECT * FROM positions WHERE contract_address = '{contract_address}'")

        if not df.empty:
            date = data[0][0]
            time = data[0][1]
            token = df['token'].iloc[0]
            mc = data[0][6]
            avg_mc = float(self.calculate_avg_mc(contract_address))
            initial_investment = float(df['initial_investment']) + actual_buy_amt
            initial_not_sold = initial_investment - float(df['sold'].iloc[0])
            unrealized_profit = self.calculate_changes(mc, avg_mc, initial_not_sold)
            remaining = initial_not_sold + unrealized_profit
            roi = self.calculate_roi(initial_investment, remaining, float(df['sold'].iloc[0]))
            data = [(date, time, df['symbol'].iloc[0], token, df['contract_address'].iloc[0], mc, avg_mc, initial_investment, remaining, float(df['sold'].iloc[0]), unrealized_profit, roi)]
            delete_open_position(contract_address)
            insert_to_db('positions', data)
        
        else:
            date = data[0][0]
            time = data[0][1]
            symbol = data[0][2]
            token = data[0][3]
            mc = data[0][6]
            initial_investment = remaining = data[0][9]
            sold = 0
            unrealized_profit = 0.0
            roi = 0.0
            data = [[date, time, symbol, token, contract_address, mc, mc, initial_investment, remaining, sold, unrealized_profit, roi]]
            insert_to_db('positions', data)

        self.settings.update_settings('balance', self.balance - buy_amt, rerun=False)

    def sell_coin(self, contract_address, sell_percentage):
        if not isinstance(sell_percentage, float):
            sell_percentage = float(sell_percentage.strip('%'))

        sell_amt = df['remaining'].iloc[0] * (sell_percentage/100)
        actual_sell_amt = sell_amt - self.priority_sell_fee
        if actual_sell_amt <= 0:
            return 'Insufficient balance to pay priority fee!'

        print("remaining to sell", sell_amt) #debug
        remaining = df['remaining'].iloc[0] - sell_amt
        data = self.add_to_trade_history(contract_address, actual_sell_amt)

        if isinstance(data, str):
            return data
        
        df = fetch_data(f"SELECT * FROM positions WHERE contract_address = '{contract_address}'")
        if sell_percentage != 100:
            date = data[0][0]
            time = data[0][1]
            symbol = data[0][2]
            token = df['token'].iloc[0]
            mc = df['market_cap'].iloc[0]
            avg_mc = df['average_market_cap'].iloc[0]
            initial_investment = float(df['initial_investment'])
            total_sold = float(df['sold'].iloc[0]) + actual_sell_amt
            initial_not_sold = initial_investment - total_sold
            unrealized_profit = self.calculate_changes(mc, avg_mc, initial_not_sold)
            remaining = initial_not_sold + unrealized_profit
            roi = self.calculate_roi(initial_investment, remaining, total_sold)
            data = [(date, time, symbol, token, df['contract_address'].iloc[0], mc, avg_mc, initial_investment, remaining, total_sold, unrealized_profit, roi)]
            delete_open_position(contract_address)
            insert_to_db('positions', data)
        else:
            date



            delete_open_position(contract_address)



        self.settings.update_settings('balance', self.balance + actual_sell_amt, rerun=False)

