# BingX Python SDK

![BingX Python SDK](https://github.com/user-attachments/assets/fa11cd06-5379-4f01-8ded-62324c8b5f19)

<div align="center">

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.8-blue?style=flat-square&logo=python)](https://www.python.org/)
[![pip](https://img.shields.io/badge/pip-latest-orange?style=flat-square&logo=pypi)](https://pypi.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/tigusigalpa/bingx-python?style=flat-square&logo=github)](https://github.com/tigusigalpa/bingx-python)

</div>

Python client for the [BingX](https://bingx.com) cryptocurrency exchange API. USDT-M and Coin-M perpetual futures, spot
trading, copy trading, sub-accounts, WebSocket streaming. **Now with API v3 support**: TWAP orders, multi-assets margin, position risk monitoring. 190+ methods.

> Also available: **[PHP SDK](https://github.com/tigusigalpa/bingx-php)** · **[Go SDK](https://github.com/tigusigalpa/bingx-go)** · **[PyPI](https://pypi.org/project/bingx-python/)**

> 📖 **[Full documentation available on Wiki](https://github.com/tigusigalpa/bingx-python/wiki)**
>
> 🚀 **[API v3 Migration Guide](API_V3_MIGRATION.md)** · **[v3 Examples](examples/api_v3_examples.py)** · **[Update Summary](API_V3_UPDATE_SUMMARY.md)**

## Table of Contents

- [Features](#features)
- [What's New in API v3](#whats-new-in-api-v3)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
    - [TWAP Service](#twap-service---algorithmic-execution-api-v3)
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
| **TWAP Service** 🆕          | Time-weighted average price algorithmic execution   | 7       |
| **Market Service**           | Market data, Quote API, symbols, prices, candles    | 44      |
| **Account Service**          | Balance, positions, leverage, margin, risk tracking | 28      |
| **Trade Service**            | Orders, multi-assets margin, auto-add margin        | 37      |
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

### API v3 Features 🆕

- **TWAP Orders** — Execute large orders without moving the market
- **Multi-Assets Margin** — Use entire portfolio as collateral
- **Position Risk Monitoring** — Real-time liquidation risk tracking
- **Income Tracking** — Detailed P&L, fees, and funding history
- **Auto-Add Margin** — Automatic margin addition to prevent liquidation
- **One-Click Reverse** — Atomically reverse position direction
- **Enhanced Market Data** — Open interest, funding rates, index prices
- **Advanced Order Types** — Trailing stops, trigger limits

### Other

- Type hints throughout
- WebSocket streams (market data, account data)
- Custom exceptions per error type
- **100% backward compatible** — All existing code works unchanged

---

## What's New in API v3

### 🎯 TWAP Orders - Trade Like Institutions

Execute large orders without moving the market. TWAP breaks your trade into smaller pieces over time.

```python
# Execute 10 BTC over 1 hour
twap = client.twap().buy(
    symbol="BTC-USDT",
    quantity=10.0,
    duration=3600,
    position_side="LONG"
)

# Monitor progress
details = client.twap().get_order_detail(twap['orderId'])
print(f"Progress: {details['executedQty']}/{details['totalQty']}")
```

### 📊 Position Risk Monitoring

Know your liquidation risk in real-time:

```python
risk = client.account().get_position_risk("BTC-USDT")
print(f"Liquidation Price: {risk['liquidationPrice']}")
print(f"Margin Ratio: {risk['marginRatio']}%")

# Track all income
income = client.account().get_income_history(
    symbol="BTC-USDT",
    income_type="REALIZED_PNL"
)
```

### 💰 Multi-Assets Margin

Use your entire portfolio as collateral:

```python
# Enable portfolio margin
client.trade().switch_multi_assets_mode(True)

# Check margin status
margin = client.trade().get_multi_assets_margin()
print(f"Total Collateral: {margin['totalCollateral']}")
print(f"Available Margin: {margin['availableMargin']}")
```

### 🛡️ Auto-Add Margin

Prevent liquidation automatically:

```python
client.trade().set_auto_add_margin(
    symbol="BTC-USDT",
    position_side="LONG",
    enabled=True
)
```

### 🔄 One-Click Position Reversal

Instantly reverse your position:

```python
# LONG → SHORT in one atomic operation
client.trade().one_click_reverse_position("BTC-USDT")
```

### 📈 Enhanced Market Data

```python
# Open interest tracking
oi = client.market().get_open_interest("BTC-USDT")

# Funding rate info
funding = client.market().get_funding_rate_info("BTC-USDT")
print(f"Rate: {funding['fundingRate']}")
```

### 🎯 Advanced Order Types

```python
# Trailing stop that locks in profits
order = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "SELL",
    "positionSide": "LONG",
    "type": "TRAILING_STOP_MARKET",
    "quantity": 1.0,
    "activationPrice": 50000,
    "callbackRate": 2.0  # Trail 2% behind peak
})
```

**📚 Full Guide**: See [API_V3_MIGRATION.md](API_V3_MIGRATION.md) for complete documentation and examples.

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

### TWAP Service - Algorithmic Execution (API v3)

Execute large orders without moving the market by breaking them into smaller pieces over time.

#### Create TWAP Orders

```python
# Buy order - execute 10 BTC over 1 hour
twap_buy = client.twap().buy(
    symbol="BTC-USDT",
    quantity=10.0,
    duration=3600,  # seconds
    position_side="LONG"
)

# Sell order with price limit
twap_sell = client.twap().sell(
    symbol="BTC-USDT",
    quantity=5.0,
    duration=1800,  # 30 minutes
    position_side="SHORT",
    price_limit=60000  # Won't execute below this price
)
```

#### Monitor TWAP Execution

```python
# Get order details and progress
details = client.twap().get_order_detail(twap_buy['orderId'])

executed = float(details['executedQty'])
total = float(details['totalQty'])
progress = (executed / total) * 100

print(f"Status: {details['status']}")
print(f"Progress: {progress:.2f}%")
print(f"Average Price: {details['avgPrice']}")

# Get all open TWAP orders
open_orders = client.twap().get_open_orders("BTC-USDT")

# Get TWAP order history
history = client.twap().get_order_history(
    symbol="BTC-USDT",
    limit=50
)
```

#### Cancel TWAP Orders

```python
# Cancel specific order
client.twap().cancel_order(twap_buy['orderId'])

# Cancel all TWAP orders for a symbol
client.twap().cancel_all_orders("BTC-USDT")
```

---

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

# Spot klines with timezone (v2 endpoint)
# time_zone: 0=UTC (default), 8=UTC+8
spot_klines = client.market().get_spot_klines(
    "BTC-USDT", "1h", 100, start_ts, end_ts, time_zone=8
)
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

#### Enhanced Market Data (API v3)

```python
# Open Interest - track total open positions
oi = client.market().get_open_interest("BTC-USDT")
print(f"Open Interest: {oi['openInterest']}")

# Open Interest History with different periods
oi_history = client.market().get_open_interest_history(
    symbol="BTC-USDT",
    period="5m",  # 5m, 15m, 30m, 1h, 4h, 1d
    limit=100
)

# Funding Rate Info - current rate and next payment time
funding = client.market().get_funding_rate_info("BTC-USDT")
print(f"Current Rate: {funding['fundingRate']}")
print(f"Next Payment: {funding['fundingTime']}")

# Index Price
index = client.market().get_index_price("BTC-USDT")
print(f"Index Price: {index['indexPrice']}")
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

#### Position Risk Monitoring (API v3)

```python
# Get detailed position risk
risk = client.account().get_position_risk("BTC-USDT")

print(f"Position Size: {risk['positionAmt']}")
print(f"Entry Price: {risk['entryPrice']}")
print(f"Mark Price: {risk['markPrice']}")
print(f"Liquidation Price: {risk['liquidationPrice']}")
print(f"Margin Ratio: {risk['marginRatio']}%")
print(f"Unrealized P&L: {risk['unrealizedProfit']}")

# Get all positions risk
all_risk = client.account().get_position_risk()
```

#### Income & Commission Tracking (API v3)

```python
# Get all income history
income = client.account().get_income_history(
    symbol="BTC-USDT",
    limit=100
)

# Filter by income type
pnl = client.account().get_income_history(
    symbol="BTC-USDT",
    income_type="REALIZED_PNL"  # Actual profits/losses
)

funding = client.account().get_income_history(
    symbol="BTC-USDT",
    income_type="FUNDING_FEE"  # 8-hour funding payments
)

# Get commission history
fees = client.account().get_commission_history(
    symbol="BTC-USDT",
    limit=100
)

# Calculate total P&L
stats = {
    'total_pnl': 0,
    'total_fees': 0,
    'total_funding': 0,
}

for record in income:
    if record['incomeType'] == 'REALIZED_PNL':
        stats['total_pnl'] += float(record['income'])
    elif record['incomeType'] == 'COMMISSION':
        stats['total_fees'] += float(record['income'])
    elif record['incomeType'] == 'FUNDING_FEE':
        stats['total_funding'] += float(record['income'])

print(f"Net P&L: ${stats['total_pnl']:.2f}")
print(f"Fees Paid: ${abs(stats['total_fees']):.2f}")
print(f"Funding: ${stats['total_funding']:.2f}")
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

#### Multi-Assets Margin (API v3)

```python
# Enable multi-assets margin mode
client.trade().switch_multi_assets_mode(True)

# Check status
mode = client.trade().get_multi_assets_mode()
print(f"Multi-assets: {'ON' if mode['multiAssetsMargin'] else 'OFF'}")

# Get margin info
margin = client.trade().get_multi_assets_margin()
print(f"Total Collateral: {margin['totalCollateral']}")
print(f"Total Margin Used: {margin['totalMargin']}")
print(f"Available Margin: {margin['availableMargin']}")
print(f"Margin Ratio: {margin['marginRatio']}%")

# Asset breakdown
for asset in margin['assets']:
    print(f"{asset['asset']}: Balance={asset['walletBalance']}, "
          f"Collateral={asset['crossMarginAsset']}")

# Get multi-assets rules (haircuts, supported assets)
rules = client.trade().get_multi_assets_rules()

# Disable multi-assets mode (only when no positions)
client.trade().switch_multi_assets_mode(False)
```

#### Auto-Add Margin (API v3)

```python
# Enable auto-add margin for LONG positions
client.trade().set_auto_add_margin(
    symbol="BTC-USDT",
    position_side="LONG",
    enabled=True
)

# Check status
status = client.trade().get_auto_add_margin("BTC-USDT", "LONG")
if status['autoAddMargin']:
    print("✅ Auto-add margin is ON")

# Disable auto-add margin
client.trade().set_auto_add_margin(
    symbol="BTC-USDT",
    position_side="LONG",
    enabled=False
)
```

#### One-Click Position Reversal (API v3)

```python
# Currently LONG 1.0 BTC
# This closes the long AND opens SHORT 1.0 BTC atomically
result = client.trade().one_click_reverse_position("BTC-USDT")
# Now you're SHORT 1.0 BTC - no gap, no slippage
```

#### Advanced Order Types (API v3)

```python
# Trailing Stop Market Order
trailing_stop = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "SELL",
    "positionSide": "LONG",
    "type": "TRAILING_STOP_MARKET",
    "quantity": 1.0,
    "activationPrice": 50000,  # Start trailing at $50k
    "callbackRate": 2.0  # Trail 2% behind peak
})

# Trigger Limit Order
trigger_limit = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "positionSide": "LONG",
    "type": "TRIGGER_LIMIT",
    "quantity": 1.0,
    "stopPrice": 48000,  # Trigger when price hits $48k
    "price": 48100  # Execute limit order at $48.1k
})

# Trailing Take Profit / Stop Loss
trailing_tp_sl = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "SELL",
    "positionSide": "LONG",
    "type": "TRAILING_TP_SL",
    "quantity": 1.0,
    "takeProfitPrice": 55000,
    "stopLossPrice": 48000,
    "trailingStopPercent": 1.5
})
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

# Internal transfer (main account internal transfer)
# wallet_type: 1=Fund Account, 2=Standard Futures, 3=Perpetual Futures, 4=Spot Account
# user_account_type: 1=UID, 2=Phone number, 3=Email
internal = client.spot_account().internal_transfer(
    coin="USDT",
    wallet_type=4,  # Spot Account
    amount=50.0,
    user_account_type=1,  # UID
    user_account="123456",
    calling_code=None,  # Required when user_account_type=2
    transfer_client_id="transfer-001",  # Optional custom ID
    recv_window=None
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
# Sub-account internal transfer
# wallet_type: 1=Fund Account, 2=Standard Futures, 3=Perpetual Futures, 15=Spot Account
# user_account_type: 1=UID, 2=Phone number, 3=Email
transfer = client.sub_account().sub_account_internal_transfer(
    coin="USDT",
    wallet_type=15,  # Spot Account
    amount=100.0,
    user_account_type=1,  # UID
    user_account="12345678",
    calling_code=None,  # Required when user_account_type=2
    transfer_client_id="transfer-001",  # Optional custom ID
    recv_window=None
)

# Sub-Mother Account Asset Transfer (master account only)
# Flexible transfer between parent and sub-accounts
transfer = client.sub_account().sub_mother_account_asset_transfer(
    asset_name="USDT",
    transfer_amount=100.0,
    from_uid=123456,
    from_type=1,  # 1=Parent account, 2=Sub-account
    from_account_type=1,  # 1=Funding, 2=Standard futures, 3=Perpetual, 15=Spot
    to_uid=789012,
    to_type=2,  # 1=Parent account, 2=Sub-account
    to_account_type=15,  # Spot account
    remark="Transfer to sub-account",
    recv_window=None
)

# Query transferable amount (master account only)
transferable = client.sub_account().get_sub_mother_account_transferable_amount(
    from_uid=123456,
    from_account_type=1,  # Funding
    to_uid=789012,
    to_account_type=15,  # Spot
    recv_window=None
)

# Query transfer history (master account only)
import time
history = client.sub_account().get_sub_mother_account_transfer_history(
    uid=123456,
    type_=None,  # Optional filter
    tran_id=None,  # Optional filter
    start_time=int(time.time() - 7*24*3600) * 1000,
    end_time=int(time.time()) * 1000,
    page_id=1,
    paging_size=50,
    recv_window=None
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
