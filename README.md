# BingX Python SDK

![BingX Python SDK](https://github.com/user-attachments/assets/fa11cd06-5379-4f01-8ded-62324c8b5f19)

<div align="center">

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.8-blue?style=flat-square&logo=python)](https://www.python.org/)
[![pip](https://img.shields.io/badge/pip-latest-orange?style=flat-square&logo=pypi)](https://pypi.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/tigusigalpa/bingx-python?style=flat-square&logo=github)](https://github.com/tigusigalpa/bingx-python)

</div>

Python client for the [BingX](https://bingx.com) cryptocurrency exchange API. USDT-M and Coin-M perpetual futures, spot
trading, copy trading, sub-accounts, WebSocket streaming. 170+ methods.

> Also available: **[PHP SDK](https://github.com/tigusigalpa/bingx-php)** · **[Go SDK](https://github.com/tigusigalpa/bingx-go)** · **[PyPI](https://pypi.org/project/bingx-python/)**

> 📖 **[Full documentation available on Wiki](https://github.com/tigusigalpa/bingx-python/wiki)**

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
    - [Market Service](#market-service---market-data)
    - [Account Service](#account-service---account-management)
    - [Trade Service](#trade-service---trading-operations)
    - [Wallet Service](#wallet-service---wallet-management)
    - [Spot Account Service](#spot-account-service---spot-account)
    - [Sub-Account Service](#sub-account-service---sub-account-management)
    - [Copy Trading Service](#copy-trading-service---copy-trading-operations)
    - [Contract Service](#contract-service---standard-futures)
    - [WebSocket API](#websocket-api)
    - [Coin-M Perpetual Futures](#coin-m-perpetual-futures---crypto-margined-contracts)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [License](#license)

---

## Features

### Supported services

| Service                      | Description                                         | Methods |
|------------------------------|-----------------------------------------------------|---------|
| **USDT-M Perpetual Futures** |                                                     |         |
| **Market Service**           | Market data, Quote API, symbols, prices, candles    | 40      |
| **Account Service**          | Balance, positions, leverage, margin, assets        | 25      |
| **Trade Service**            | Orders, trade history, position management          | 30      |
| **Wallet Service**           | Deposits, withdrawals, wallet addresses             | 5       |
| **Spot Account Service**     | Spot balance, transfers, internal transfers         | 7       |
| **Sub-Account Service**      | Sub-account management, API keys, transfers         | 20      |
| **Copy Trading Service**     | Copy trading for futures and spot                   | 13      |
| **Contract Service**         | Standard contract API                               | 3       |
| **Listen Key Service**       | WebSocket authentication                            | 3       |
| **Coin-M Perpetual Futures** |                                                     |         |
| **Coin-M Market**            | Contract info, ticker, depth, klines, open interest | 6       |
| **Coin-M Trade**             | Orders, positions, leverage, margin, balance        | 17      |
| **Coin-M Listen Key**        | WebSocket authentication for Coin-M                 | 3       |

### Security

- HMAC-SHA256 request signing
- Automatic timestamp validation
- base64 and hex signature encoding
- recvWindow for replay attack protection

### Other

- Type hints throughout
- WebSocket streams (market data, account data)
- Custom exceptions per error type

---

## Quick Start

```python
from bingx import BingXClient

client = BingXClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Price
price = client.market().get_latest_price("BTC-USDT")

# Balance
balance = client.account().get_balance()

# Order
order = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.001
})
```

---

## Installation

### Requirements

- Python >= 3.8

### pip

```bash
pip install bingx-python
```

### From source

```bash
git clone https://github.com/tigusigalpa/bingx-python.git
cd bingx-python
pip install -e .
```

### API keys

1. Go to [BingX API Settings](https://bingx.com/en-US/accounts/api)
2. Click "Create API"
3. Save **API Key** and **Secret Key**
4. Configure access rights
5. Secret Key is shown only once

---

## Usage

### Market Service - Market Data

#### Symbols

```python
all_symbols = client.market().get_all_symbols()
# {'spot': [...], 'futures': [...]}

spot_symbols = client.market().get_spot_symbols()

futures_symbols = client.market().get_futures_symbols()
```

#### Prices

```python
futures_price = client.market().get_latest_price("BTC-USDT")
spot_price = client.market().get_spot_latest_price("BTC-USDT")

ticker = client.market().get_24hr_ticker("BTC-USDT")
spot_ticker = client.market().get_spot_24hr_ticker("BTC-USDT")

# All tickers
all_tickers = client.market().get_24hr_ticker()
```

#### Depth and Klines

```python
depth = client.market().get_depth("BTC-USDT", 20)
spot_depth = client.market().get_spot_depth("BTC-USDT", 20)

klines = client.market().get_klines("BTC-USDT", "1h", 100)
spot_klines = client.market().get_spot_klines("BTC-USDT", "1h", 100)

# With time range
import time
start_ts = int(time.mktime(time.strptime("2024-01-01", "%Y-%m-%d")) * 1000)
end_ts = int(time.mktime(time.strptime("2024-01-02", "%Y-%m-%d")) * 1000)
klines = client.market().get_klines("BTC-USDT", "1h", 100, start_ts, end_ts)
```

#### Funding Rate, Mark Price

```python
funding_rate = client.market().get_funding_rate_history("BTC-USDT", 100)
mark_price = client.market().get_mark_price("BTC-USDT")
premium_klines = client.market().get_premium_index_klines("BTC-USDT", "1h", 100)
continuous_klines = client.market().get_continuous_klines("BTC-USDT", "1h", 100)
```

#### Trades

```python
agg_trades = client.market().get_aggregate_trades("BTC-USDT", 500)
recent_trades = client.market().get_recent_trades("BTC-USDT", 500)

spot_agg_trades = client.market().get_spot_aggregate_trades("BTC-USDT", 500)
spot_recent_trades = client.market().get_spot_recent_trades("BTC-USDT", 500)
```

#### Sentiment

```python
long_short_ratio = client.market().get_top_long_short_ratio("BTC-USDT", 10)
historical_ratio = client.market().get_historical_top_long_short_ratio(
    "BTC-USDT", 500, start_ts, end_ts
)
basis = client.market().get_basis("BTC-USDT", "PERPETUAL", 100)
```

#### Quote API

```python
contracts = client.market().get_contracts()
quote_depth = client.market().get_quote_depth("BTC-USDT", 20)
book_ticker = client.market().get_book_ticker("BTC-USDT")
quote_ticker = client.market().get_quote_ticker("BTC-USDT")
funding = client.market().get_quote_funding_rate("BTC-USDT")
oi = client.market().get_quote_open_interest("BTC-USDT")
premium = client.market().get_premium_index("BTC-USDT")
quote_trades = client.market().get_quote_trades("BTC-USDT", 100)
klines_v3 = client.market().get_klines_v3("BTC-USDT", "1h", 500)
rules = client.market().get_trading_rules("BTC-USDT")
```

---

### Account Service - Account Management

#### Balance and Positions

```python
balance = client.account().get_balance()
all_positions = client.account().get_positions()
positions = client.account().get_positions("BTC-USDT")
account_info = client.account().get_account_info()
```

#### Leverage and Margin

```python
leverage = client.account().get_leverage("BTC-USDT")
client.account().set_leverage("BTC-USDT", "BOTH", 20)

margin_mode = client.account().get_margin_mode("BTC-USDT")
client.account().set_margin_mode("BTC-USDT", "ISOLATED")

client.account().set_position_margin("BTC-USDT", "LONG", 100.0, 1)
```

#### Fees

```python
fees = client.account().get_trading_fees("BTC-USDT")
permissions = client.account().get_account_permissions()
rate_limits = client.account().get_api_rate_limits()
```

---

### Trade Service - Trading Operations

#### Quick Methods

```python
# Spot
buy = client.trade().spot_market_buy("BTC-USDT", 0.001)
sell = client.trade().spot_market_sell("BTC-USDT", 0.001)
limit_buy = client.trade().spot_limit_buy("BTC-USDT", 0.001, 50000)
limit_sell = client.trade().spot_limit_sell("BTC-USDT", 0.001, 60000)

# Futures
long_order = client.trade().futures_long_market("BTC-USDT", 100, 10)
short_order = client.trade().futures_short_market("BTC-USDT", 100, 10)

long_limit = client.trade().futures_long_limit(
    "BTC-USDT", 100, 50000, 48000, 55000, 10
)
```

#### Orders

```python
order = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.001
})

test_order = client.trade().create_test_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "type": "LIMIT",
    "quantity": 0.001,
    "price": 50000
})

batch = client.trade().create_batch_orders([
    {"symbol": "BTC-USDT", "side": "BUY", "type": "LIMIT", "quantity": 0.001, "price": 50000},
    {"symbol": "ETH-USDT", "side": "SELL", "type": "LIMIT", "quantity": 0.01, "price": 3000}
])
```

#### Cancel

```python
client.trade().cancel_order("BTC-USDT", "123456789")
client.trade().cancel_all_orders("BTC-USDT")
client.trade().cancel_batch_orders("BTC-USDT", ["123456789", "987654321"])
client.trade().cancel_and_replace_order("BTC-USDT", "123456789", "BUY", "LIMIT", 0.001, 50000)
```

#### History

```python
order = client.trade().get_order("BTC-USDT", "123456789")
open_orders = client.trade().get_open_orders("BTC-USDT")
history = client.trade().get_order_history("BTC-USDT", 100)
trades = client.trade().get_user_trades("BTC-USDT", 100)
```

#### Positions

```python
mode = client.trade().get_position_mode()
client.trade().set_position_mode("HEDGE_MODE")
client.trade().close_all_positions("BTC-USDT")
client.trade().change_margin_type("BTC-USDT", "ISOLATED")
```

---

### Wallet Service - Wallet Management

```python
deposits = client.wallet().get_deposit_history(coin="USDT", status=1)
address = client.wallet().get_deposit_address("USDT", "TRC20")
withdrawals = client.wallet().get_withdrawal_history(coin="USDT")

withdrawal = client.wallet().withdraw(
    coin="USDT",
    address="TXxx...xxx",
    amount=100.0,
    network="TRC20"
)

coins = client.wallet().get_all_coin_info()
```

---

### Spot Account Service - Spot Account

```python
balance = client.spot_account().get_balance()
fund_balance = client.spot_account().get_fund_balance()

transfer = client.spot_account().universal_transfer(
    type_="FUND_PFUTURES", asset="USDT", amount=100.0
)

history = client.spot_account().get_asset_transfer_records(type_="FUND_PFUTURES")

internal = client.spot_account().internal_transfer(
    coin="USDT", wallet_type="SPOT", amount=50.0,
    transfer_type="FROM_MAIN_TO_SUB", sub_uid="123456"
)

all_balances = client.spot_account().get_all_account_balances()
```

---

### Sub-Account Service - Sub-Account Management

#### Sub-Accounts

```python
client.sub_account().create_sub_account("sub_account_001")
sub_accounts = client.sub_account().get_sub_account_list()
assets = client.sub_account().get_sub_account_assets("12345678")
client.sub_account().update_sub_account_status("sub_account_001", 1)  # 1: enable, 2: disable
```

#### API Keys

```python
api_key = client.sub_account().create_sub_account_api_key(
    sub_account_string="sub_account_001",
    label="Trading Bot",
    permissions={"spot": True, "futures": True},
    ip="192.168.1.1"
)

api_keys = client.sub_account().query_api_key("sub_account_001")
client.sub_account().delete_sub_account_api_key("sub_account_001", "your_api_key")
```

#### Transfers

```python
transfer = client.sub_account().sub_account_internal_transfer(
    coin="USDT", wallet_type="SPOT", amount=100.0,
    transfer_type="FROM_MAIN_TO_SUB", to_sub_uid="12345678"
)

records = client.sub_account().get_sub_account_internal_transfer_records()
```

---

### Copy Trading Service - Copy Trading Operations

#### Futures

```python
orders = client.copy_trading().get_current_track_orders("BTC-USDT")
client.copy_trading().close_track_order("1252864099381234567")

client.copy_trading().set_tpsl(
    position_id="1252864099381234567",
    stop_loss=48000.0,
    take_profit=52000.0
)

details = client.copy_trading().get_trader_detail()
summary = client.copy_trading().get_profit_summary()
profits = client.copy_trading().get_profit_detail(page_index=1, page_size=20)
client.copy_trading().set_commission(5.0)
pairs = client.copy_trading().get_trading_pairs()
```

#### Spot

```python
client.copy_trading().sell_spot_order("1253517936071234567")
details = client.copy_trading().get_spot_trader_detail()
summary = client.copy_trading().get_spot_profit_summary()
history = client.copy_trading().get_spot_history_orders()
```

---

### Contract Service - Standard Futures

```python
positions = client.contract().get_all_positions()
orders = client.contract().get_all_orders(symbol="BTC-USDT", limit=100)
balance = client.contract().get_balance()
```

---

### WebSocket API

#### Market Data Stream

```python
from bingx.websocket import MarketDataStream

stream = MarketDataStream()
stream.connect()

stream.subscribe_trade("BTC-USDT")
stream.subscribe_kline("BTC-USDT", "1m")
stream.subscribe_depth("BTC-USDT", 20)
stream.subscribe_ticker("BTC-USDT")
stream.subscribe_book_ticker("BTC-USDT")

def on_message(data):
    if "dataType" in data:
        if data["dataType"] == "BTC-USDT@trade":
            print(f"Trade: {data['data']['p']}")
        elif data["dataType"] == "BTC-USDT@kline_1m":
            print("Kline update")

stream.on_message(on_message)
stream.listen()  # blocking
# stream.listen_async()  # non-blocking

stream.unsubscribe_trade("BTC-USDT")
stream.disconnect()
```

#### Account Data Stream

```python
from bingx.websocket import AccountDataStream

# Get listen key
response = client.listen_key().generate()
listen_key = response["listenKey"]

stream = AccountDataStream(listen_key)
stream.connect()

stream.on_balance_update(lambda b: print(f"Balance: {b}"))
stream.on_position_update(lambda p: print(f"Position: {p}"))
stream.on_order_update(lambda o: print(f"Order: {o}"))

stream.listen_async()

# Extend every 30 min
client.listen_key().extend(listen_key)

# Close
client.listen_key().delete(listen_key)
stream.disconnect()
```

#### Listen Key

```python
response = client.listen_key().generate()    # valid 60 min
client.listen_key().extend(listen_key)       # extend
client.listen_key().delete(listen_key)       # delete
```

---

### Coin-M Perpetual Futures - Crypto-Margined Contracts

Coin-M futures are margined and settled in cryptocurrency (BTC, ETH, etc.) instead of USDT. API path:
`/openApi/cswap/v1/`.

| Feature             | USDT-M Futures      | Coin-M Futures                  |
|---------------------|---------------------|---------------------------------|
| **Margin Currency** | USDT (stablecoin)   | Cryptocurrency (BTC, ETH, etc.) |
| **Settlement**      | USDT                | Base cryptocurrency             |
| **API Path**        | `/openApi/swap/v2/` | `/openApi/cswap/v1/`            |
| **Symbol Format**   | BTC-USDT            | BTC-USD, ETH-USD                |

#### Market Data

```python
contracts = client.coinm().market().get_contracts()
ticker = client.coinm().market().get_ticker("BTC-USD")
depth = client.coinm().market().get_depth("BTC-USD", 20)
klines = client.coinm().market().get_klines("BTC-USD", "1h", 100)
oi = client.coinm().market().get_open_interest("BTC-USD")
funding = client.coinm().market().get_funding_rate("BTC-USD")
```

#### Trading

```python
order = client.coinm().trade().create_order({
    "symbol": "BTC-USD",
    "side": "BUY",
    "positionSide": "LONG",
    "type": "MARKET",
    "quantity": 100
})

positions = client.coinm().trade().get_positions("BTC-USD")
balance = client.coinm().trade().get_balance()
client.coinm().trade().set_leverage("BTC-USD", "BOTH", 20)
client.coinm().trade().cancel_order("BTC-USD", "order_id")
```

---

## Error Handling

```python
from bingx.exceptions import (
    BingXException,
    APIException,
    AuthenticationException,
    RateLimitException,
    InsufficientBalanceException
)

try:
    balance = client.account().get_balance()
except AuthenticationException as e:
    print(f"Auth: {e}")
except RateLimitException as e:
    print(f"Rate limit: {e}")
except InsufficientBalanceException as e:
    print(f"Balance: {e}")
except APIException as e:
    print(f"API: {e}")
except BingXException as e:
    print(f"Error: {e}")
```

Exception hierarchy:

| Exception                      | When                                    |
|--------------------------------|-----------------------------------------|
| `BingXException`               | Base, network errors, invalid responses |
| `APIException`                 | API returned error code                 |
| `AuthenticationException`      | Invalid API key/secret (100001–100004)  |
| `RateLimitException`           | Too many requests (100005)              |
| `InsufficientBalanceException` | Not enough funds (200001)               |

---

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
pytest tests/ --cov=bingx
```

---

## License

MIT — see [LICENSE](LICENSE).

## Author

**Igor Sazonov** — [sovletig@gmail.com](mailto:sovletig@gmail.com) — [@tigusigalpa](https://github.com/tigusigalpa)

## Contributing

1. Fork
2. `git checkout -b feature/name`
3. `git commit -m 'Add feature'`
4. `git push origin feature/name`
5. Open Pull Request
