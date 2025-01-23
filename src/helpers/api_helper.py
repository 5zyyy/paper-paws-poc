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
            if response.status_code == 429:
                return f'Too many request made to CoinGecko API! (Status Code: {response.status_code})'
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
                print(f"token_data:\n{details}")
                return details
            except Exception as e:
                return 'Contract Address is invalid!'
        else:
            return f'{response.text} (Status Code: {response.status_code})'
        
    def get_multiple_token_data(self, contract_address):
        url = "https://streaming.bitquery.io/eap"

        query = """
        query GetDEXTradeAndTokenSupply($mintAddresses: [String!]) {
        Solana {
            DEXTrades( 
            orderBy: { descending: Block_Time }
            where: {
                Trade: {
                Buy: { Currency: { MintAddress: { in: $mintAddresses } } }
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
            orderBy: { descending: Block_Time }
            where: {
                TokenSupplyUpdate: { Currency: { MintAddress: { in: $mintAddresses } } }
            }
            ) {
            TokenSupplyUpdate {
                Currency{
                    MintAddress
                }
                PostBalance
            }
            }
        }
        }

        """

        variables = {
            "mintAddresses": contract_address
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
            num_of_ca = len(contract_address)
            data = response.json()

            dex_trades = data['data']['Solana']['DEXTrades']
            token_supply_updates = data['data']['Solana']['TokenSupplyUpdates']

            latest_trades = {}
            latest_balances = {}

            added_count = 0
            for trade in dex_trades:
                mint_address = trade['Trade']['Buy']['Currency']['MintAddress']

                if mint_address not in latest_trades:
                    latest_trades[mint_address] = {
                        'token_name' : trade['Trade']['Buy']['Currency']['Name'],
                        'token_symbol': trade['Trade']['Buy']['Currency']['Symbol'],
                        'token_price': trade['Trade']['Buy']['PriceInUSD']
                    }
                    added_count += 1
                    if added_count == num_of_ca:
                        break
            
            added_count = 0
            for supply_update in token_supply_updates:
                mint_address = supply_update['TokenSupplyUpdate']['Currency']['MintAddress']

                if mint_address not in latest_balances:
                    latest_balances[mint_address] = supply_update['TokenSupplyUpdate']['PostBalance']
                    added_count += 1
                    if added_count == num_of_ca:
                        break

            details = {}
            for mint_address, trade in latest_trades.items():
                token_name = trade['token_name']
                token_symbol = trade['token_symbol']
                token_price = float(trade['token_price'])
                token_supply = float(latest_balances.get(mint_address, 0))
                market_cap = token_supply * token_price

                details[mint_address] = {
                    'name': token_name,
                    'symbol': token_symbol,
                    'market_cap': market_cap,
                    'token_price': token_price
                }

            print(f"get_multiple_token_data:\n{details}")
            return details
        else:
            return f'{response.text} (Status Code: {response.status_code})'