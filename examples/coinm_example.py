"""
Coin-M Perpetual Futures Example

Demonstrates Coin-M (crypto-margined) futures trading.
"""

from bingx import BingXClient
from bingx.exceptions import BingXException

# Initialize client
client = BingXClient(
    api_key="your_api_key_here",
    api_secret="your_api_secret_here"
)

try:
    # Get Coin-M contracts
    contracts = client.coinm().market().get_contracts()
    print(f"Coin-M Contracts: {contracts}")

    # Get ticker for BTC-USD
    ticker = client.coinm().market().get_ticker("BTC-USD")
    print(f"BTC-USD Ticker: {ticker}")

    # Get order book
    depth = client.coinm().market().get_depth("BTC-USD", 20)
    print(f"Depth: {depth}")

    # Get candlesticks
    klines = client.coinm().market().get_klines("BTC-USD", "1h", 10)
    print(f"Klines: {klines}")

    # Get open interest
    open_interest = client.coinm().market().get_open_interest("BTC-USD")
    print(f"Open Interest: {open_interest}")

    # Get funding rate
    funding_rate = client.coinm().market().get_funding_rate("BTC-USD")
    print(f"Funding Rate: {funding_rate}")

    # Get balance
    balance = client.coinm().trade().get_balance()
    print(f"Coin-M Balance: {balance}")

    # Get positions
    positions = client.coinm().trade().get_positions("BTC-USD")
    print(f"Positions: {positions}")

    # Set leverage
    leverage_result = client.coinm().trade().set_leverage("BTC-USD", "BOTH", 10)
    print(f"Leverage set: {leverage_result}")

    # Create order
    order = client.coinm().trade().create_order({
        "symbol": "BTC-USD",
        "side": "BUY",
        "positionSide": "LONG",
        "type": "MARKET",
        "quantity": 100
    })
    print(f"Order created: {order}")

    # Get open orders
    open_orders = client.coinm().trade().get_open_orders("BTC-USD")
    print(f"Open orders: {open_orders}")

except BingXException as e:
    print(f"Error: {e}")
