"""
Basic Usage Example

Demonstrates basic usage of the BingX Python SDK.
"""

from bingx import BingXClient

# Initialize client
client = BingXClient(
    api_key="your_api_key_here",
    api_secret="your_api_secret_here",
    signature_encoding="base64"  # or "hex"
)

# Get current BTC price
price = client.market().get_latest_price("BTC-USDT")
print(f"BTC Price: {price}")

# Get account balance
balance = client.account().get_balance()
print(f"Balance: {balance}")

# Get all positions
positions = client.account().get_positions()
print(f"Positions: {positions}")

# Get market depth
depth = client.market().get_depth("BTC-USDT", 20)
print(f"Depth: {depth}")

# Get 24hr ticker
ticker = client.market().get_24hr_ticker("BTC-USDT")
print(f"24hr Ticker: {ticker}")

# Get candlestick data
klines = client.market().get_klines("BTC-USDT", "1h", 10)
print(f"Klines: {klines}")
