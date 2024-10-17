from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv
load_dotenv()

# Set up logging (optional)
import logging
logging.basicConfig(filename="pybit.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")
print(api_key)
print(api_secret)



TESTNET = True  # True means your API keys were generated on testnet.bybit.com


# Create direct HTTP session instance

session = HTTP(
    api_key=api_key,
    api_secret=api_secret,
    testnet=TESTNET,
)

# Place order

response = session.place_order(
    category="spot",
    symbol="ETHUSDT",
    side="Sell",
    orderType="Market",
    qty="0.01",
    timeInForce="GTC",
)

# Example to cancel orders

response = session.get_open_orders(
    category="linear",
    symbol="BTCUSDT",
)

orders = response["result"]["list"]

for order in orders:
    if order["orderStatus"] == "Untriggered":
        session.cancel_order(
            category="linear",
            symbol=order["symbol"],
            orderId=order["orderId"],
        )


# Batch cancel orders

orders_to_cancel = [
    {"category": "option", "symbol": o["symbol"], "orderId": o["orderId"]}
    for o in response["result"]["list"]
    if o["orderStatus"] == "New"
]

response = session.cancel_batch_order(
    category="option",
    request=orders_to_cancel,
)