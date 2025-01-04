import requests

class QueryAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_details(self, contract_address=None):
        if contract_address is None:
            url = 'https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd'
        else:
            url = f"https://api.coingecko.com/api/v3/coins/solana/contract/{contract_address}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json() 
            return data
        else:
            return response.status_code