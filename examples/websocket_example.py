"""
WebSocket Example

Demonstrates WebSocket usage for real-time data.
"""

import time
from bingx import BingXClient
from bingx.websocket import MarketDataStream, AccountDataStream

# Initialize client
client = BingXClient(
    api_key="your_api_key_here",
    api_secret="your_api_secret_here"
)

# Example 1: Market Data Stream
print("=== Market Data Stream Example ===")

market_stream = MarketDataStream()
market_stream.connect()

# Subscribe to multiple streams
market_stream.subscribe_trade("BTC-USDT")
market_stream.subscribe_kline("BTC-USDT", "1m")
market_stream.subscribe_depth("BTC-USDT", 20)
market_stream.subscribe_ticker("BTC-USDT")

def on_market_message(data):
    if "dataType" in data:
        data_type = data["dataType"]
        if "@trade" in data_type:
            print(f"Trade: {data['data']}")
        elif "@kline" in data_type:
            print(f"Kline: {data['data']}")
        elif "@depth" in data_type:
            print(f"Depth update received")
        elif "@ticker" in data_type:
            print(f"Ticker: {data['data']}")

market_stream.on_message(on_market_message)

# Listen asynchronously
market_stream.listen_async()

# Let it run for 30 seconds
time.sleep(30)

# Disconnect
market_stream.disconnect()

print("\n=== Account Data Stream Example ===")

# Example 2: Account Data Stream
# Generate listen key
listen_key_response = client.listen_key().generate()
listen_key = listen_key_response["listenKey"]

account_stream = AccountDataStream(listen_key)
account_stream.connect()

def on_balance_update(balances):
    print(f"Balance update: {balances}")

def on_position_update(positions):
    print(f"Position update: {positions}")

def on_order_update(order):
    print(f"Order update: {order}")

account_stream.on_balance_update(on_balance_update)
account_stream.on_position_update(on_position_update)
account_stream.on_order_update(on_order_update)

# Listen asynchronously
account_stream.listen_async()

# Let it run for 30 seconds
time.sleep(30)

# Extend listen key (should be done every 30 minutes)
client.listen_key().extend(listen_key)

# Disconnect
client.listen_key().delete(listen_key)
account_stream.disconnect()

print("WebSocket examples completed")
