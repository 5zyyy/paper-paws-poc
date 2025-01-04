import requests

class QueryAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_sol_price(self):
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() 
            return data
        else:
            return f'Error! (Status Code: {response.status_code})'

    def token_data(self, contract_address):
        url = "https://streaming.bitquery.io/eap"

        query = """
        query GetDEXTradeAndTokenSupply($mintAddress: String!) {
        Solana {
            DEXTrades(
            limit: { count: 1 }
            orderBy: { descending: Block_Time }
            where: {
                Trade: {
                Buy: { Currency: { MintAddress: { is: $mintAddress } } }
                Dex: { ProtocolName: { is: "pump" } }
                }
                Transaction: { Result: { Success: true } }
            }
            ) {
            Trade {
                Buy {
                PriceInUSD
                Currency {
                    Name
                    Symbol
                    MintAddress
                }
                }
            }
            }
            TokenSupplyUpdates(
            limit: { count: 1 }
            orderBy: { descending: Block_Time }
            where: { TokenSupplyUpdate: { Currency: { MintAddress: { is: $mintAddress } } } }
            ) {
            TokenSupplyUpdate {
                PostBalance
            }
            }
        }
        }
        """

        variables = {
            "mintAddress": contract_address
        }

        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }

        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            try:
                token_supply = float(data['data']['Solana']['TokenSupplyUpdates'][0]['TokenSupplyUpdate']['PostBalance'])
                token_price = data['data']['Solana']['DEXTrades'][0]['Trade']['Buy']['PriceInUSD']
                market_cap = token_supply * token_price
                details = {
                    'name': data['data']['Solana']['DEXTrades'][0]['Trade']['Buy']['Currency']['Name'],
                    'symbol': data['data']['Solana']['DEXTrades'][0]['Trade']['Buy']['Currency']['Symbol'],
                    'market_cap': market_cap,
                    'token_price': token_price
                }
                return details
            except Exception as e:
                return 'Contract Address is invalid!'
        else:
            return f'{response.text} (Status Code: {response.status_code})'