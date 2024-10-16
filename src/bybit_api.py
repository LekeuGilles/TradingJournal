
import requests
import time
import hmac
import hashlib

API_URL = "https://api.bybit.com"  # Main API endpoint

def generate_signature(api_key, api_secret, params):
    """Generate a signature for API requests."""
    params['api_key'] = api_key
    params['timestamp'] = str(int(time.time() * 1000))
    # Create a sorted query string
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    # Generate the signature
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def get_wallet_balance(api_key, api_secret):
    """Get the wallet balance."""
    params = {
        'accountType': 'UNIFIED'  # Specify the account type
    }
    params['sign'] = generate_signature(api_key, api_secret, params)

    response = requests.get(f"{API_URL}/v5/account/wallet-balance", params=params)

    print("Request URL:", response.url)  # Print the request URL for debugging
    print("Response Status Code:", response.status_code)  # Print the status code

    if response.status_code == 200:
        data = response.json()
        print("Response Data:", data)  # Print the entire response for debugging
        if 'result' in data:
            balances = data['result']['list']  # Get the list of balances
            return balances  # Return the wallet balance information
        else:
            print("Error in fetching wallet balance:", data)
            return None
    else:
        print("HTTP Error:", response.status_code, response.text)  # Print response text for debugging
        return None


# Example usage:
if __name__ == "__main__":
    API_KEY = "..."
    API_SECRET = ".."
    wallet_balance = get_wallet_balance(API_KEY, API_SECRET)
    if wallet_balance:
        for coin_info in wallet_balance:
            coin = coin_info['coin']
            wallet_balance = coin_info['totalEquity']
            print(f" TESTRETS: {coin} Wallet Balance: {wallet_balance}")

