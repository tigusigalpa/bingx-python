# BingX Python SDK - Quick Start Guide

## Installation

```bash
pip install bingx-python
```

## Basic Setup

```python
from bingx import BingXClient

# Initialize the client
client = BingXClient(
    api_key="your_api_key_here",
    api_secret="your_api_secret_here",
    signature_encoding="base64"  # or "hex"
)
```

## Common Operations

### 1. Get Market Data

```python
# Get current BTC price
price = client.market().get_latest_price("BTC-USDT")
print(f"BTC Price: {price['data']['price']}")

# Get 24hr ticker
ticker = client.market().get_24hr_ticker("BTC-USDT")

# Get order book
depth = client.market().get_depth("BTC-USDT", 20)

# Get candlesticks
klines = client.market().get_klines("BTC-USDT", "1h", 100)
```

### 2. Account Information

```python
# Get balance
balance = client.account().get_balance()

# Get positions
positions = client.account().get_positions()

# Set leverage
client.account().set_leverage("BTC-USDT", "BOTH", 10)
```

### 3. Place Orders

```python
# Market order
order = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.001
})

# Limit order
limit_order = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "type": "LIMIT",
    "quantity": 0.001,
    "price": 50000
})

# Quick methods
client.trade().spot_market_buy("BTC-USDT", 0.001)
client.trade().futures_long_market("BTC-USDT", 100, 10)
```

### 4. Manage Orders

```python
# Get open orders
open_orders = client.trade().get_open_orders("BTC-USDT")

# Cancel order
client.trade().cancel_order("BTC-USDT", "order_id")

# Cancel all orders
client.trade().cancel_all_orders("BTC-USDT")
```

### 5. WebSocket Streaming

```python
from bingx.websocket import MarketDataStream

# Create stream
stream = MarketDataStream()
stream.connect()

# Subscribe to data
stream.subscribe_trade("BTC-USDT")
stream.subscribe_kline("BTC-USDT", "1m")

# Handle messages
def on_message(data):
    print(f"Received: {data}")

stream.on_message(on_message)
stream.listen_async()
```

### 6. Coin-M Futures

```python
# Get Coin-M ticker
ticker = client.coinm().market().get_ticker("BTC-USD")

# Create Coin-M order
order = client.coinm().trade().create_order({
    "symbol": "BTC-USD",
    "side": "BUY",
    "positionSide": "LONG",
    "type": "MARKET",
    "quantity": 100
})
```

## Error Handling

```python
from bingx.exceptions import (
    BingXException,
    AuthenticationException,
    RateLimitException
)

try:
    balance = client.account().get_balance()
except AuthenticationException as e:
    print(f"Auth error: {e}")
except RateLimitException as e:
    print(f"Rate limit: {e}")
except BingXException as e:
    print(f"Error: {e}")
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/](examples/) for more code samples
- Visit [BingX API Documentation](https://bingx-api.github.io/docs/)

## Getting API Keys

1. Visit [BingX API Settings](https://bingx.com/en-US/accounts/api)
2. Create new API key
3. Save your API Key and Secret Key securely
4. Configure appropriate permissions

## Support

- GitHub Issues: https://github.com/tigusigalpa/bingx-python/issues
- Email: sovletig@gmail.com
