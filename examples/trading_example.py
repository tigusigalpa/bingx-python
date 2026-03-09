"""
Trading Example

Demonstrates trading operations with the BingX Python SDK.
"""

from bingx import BingXClient
from bingx.exceptions import BingXException

# Initialize client
client = BingXClient(
    api_key="your_api_key_here",
    api_secret="your_api_secret_here"
)

try:
    # Create a market buy order
    order = client.trade().create_order({
        "symbol": "BTC-USDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 0.001
    })
    print(f"Market order created: {order}")

    # Create a limit order
    limit_order = client.trade().create_order({
        "symbol": "BTC-USDT",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": 0.001,
        "price": 50000
    })
    print(f"Limit order created: {limit_order}")

    # Get open orders
    open_orders = client.trade().get_open_orders("BTC-USDT")
    print(f"Open orders: {open_orders}")

    # Cancel an order
    if open_orders.get("data"):
        order_id = open_orders["data"][0]["orderId"]
        cancel_result = client.trade().cancel_order("BTC-USDT", order_id)
        print(f"Order cancelled: {cancel_result}")

    # Get order history
    history = client.trade().get_order_history("BTC-USDT", 10)
    print(f"Order history: {history}")

    # Set leverage
    leverage_result = client.account().set_leverage("BTC-USDT", "BOTH", 10)
    print(f"Leverage set: {leverage_result}")

    # Get positions
    positions = client.account().get_positions("BTC-USDT")
    print(f"Positions: {positions}")

except BingXException as e:
    print(f"Error: {e}")
