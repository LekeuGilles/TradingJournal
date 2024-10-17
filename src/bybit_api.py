import os
import requests
import time
import hmac
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv

API_URL = "https://api.bybit.com"  # Main API endpoint

load_dotenv()

def generate_signature(api_key, api_secret, params):
    """Generate a signature for API requests."""
    params['api_key'] = api_key
    params['timestamp'] = str(int(time.time() * 1000))
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def get_wallet_balance(api_key, api_secret):
    """Get the wallet balance."""
    params = {
        'accountType': 'UNIFIED'
    }
    params['sign'] = generate_signature(api_key, api_secret, params)
    response = requests.get(f"{API_URL}/v5/account/wallet-balance", params=params)
    if response.status_code == 200:
        data = response.json()
        print("Response Data:", data)
        return data
    else:
        print("HTTP Error:", response.status_code, response.text)
        return None


def parse_wallet_balances(data):
    """Parse the wallet balance data to extract individual coin balances and their total USD values."""
    try:
        # Debugging output to check what is being passed to the function
        print("Debug - Raw Data Passed to Function:", data)

        # Accessing the list of coins correctly
        coin_balances = data.get('result', {}).get('list', [])[0].get('coin', [])

        total_values = {}
        total_usd_value = 0  # Initialize total USD value

        for coin in coin_balances:
            coin_type = coin.get('coin')
            usd_value = float(coin.get('usdValue', 0))  # Default to 0 if not found
            wallet_balance = float(coin.get('walletBalance', 0))  # Default to 0 if not found

            # Storing and accumulating values
            total_values[coin_type] = {'wallet_balance': wallet_balance, 'usd_value': usd_value}
            total_usd_value += usd_value

        # Return both the detailed coin values and the total USD value
        return total_values, total_usd_value

    except Exception as e:
        print("Error processing wallet balances:", e)
        return {}, 0  # Return empty results in case of error


if __name__ == "__main__":
    API_KEY = os.getenv("BYBIT_API_KEY")
    API_SECRET = os.getenv("BYBIT_API_SECRET")

    # Fetch and print wallet balance
    wallet_data = get_wallet_balance(API_KEY, API_SECRET)
    if wallet_data:
        coin_values, total_portfolio_value = parse_wallet_balances(wallet_data)
        for coin, values in coin_values.items():
            print(f"{coin} Wallet Balance: {values['wallet_balance']} with a Total Value of {values['usd_value']} USDT")
        print(f"Total Portfolio Value in USDT: {total_portfolio_value} USDT")
    else:
        print("Failed to fetch wallet balance.")
