# BingX Python SDK - API v3 Migration Guide

## Overview

This guide covers the migration from BingX API v1/v2 to v3. The good news: **your existing code still works**. All v3 features are opt-in additions.

## What's New in API v3

### 1. Enhanced Market Data

New endpoints for institutional-grade market analysis:

```python
# Open Interest - track total open positions
oi = client.market().get_open_interest("BTC-USDT")
print(f"Open Interest: {oi['openInterest']}")

# Open Interest History
oi_history = client.market().get_open_interest_history(
    symbol="BTC-USDT",
    period="5m",  # 5m, 15m, 30m, 1h, 4h, 1d
    limit=100
)

# Funding Rate Info
funding = client.market().get_funding_rate_info("BTC-USDT")
print(f"Current Rate: {funding['fundingRate']}")
print(f"Next Payment: {funding['fundingTime']}")

# Book Ticker - best bid/ask without full depth
ticker = client.market().get_book_ticker("BTC-USDT")
print(f"Best Bid: {ticker['bidPrice']} @ {ticker['bidQty']}")
print(f"Best Ask: {ticker['askPrice']} @ {ticker['askQty']}")

# Index Price
index = client.market().get_index_price("BTC-USDT")
print(f"Index: {index['indexPrice']}")
```

### 2. Position Risk Monitoring

Real-time risk metrics to prevent liquidations:

```python
# Get detailed position risk
risk = client.account().get_position_risk("BTC-USDT")

print(f"Position Size: {risk['positionAmt']}")
print(f"Entry Price: {risk['entryPrice']}")
print(f"Mark Price: {risk['markPrice']}")
print(f"Liquidation Price: {risk['liquidationPrice']}")
print(f"Margin Ratio: {risk['marginRatio']}%")
print(f"Unrealized P&L: {risk['unrealizedProfit']}")

# Monitor risk in real-time
import time

while True:
    risk = client.account().get_position_risk("BTC-USDT")
    
    if float(risk['marginRatio']) > 80:
        print(f"⚠️ WARNING: Margin at {risk['marginRatio']}%!")
        # Take action: add margin, close positions, etc.
    
    time.sleep(60)
```

### 3. Income & Commission Tracking

Track every dollar in and out:

```python
# Get all income types
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

# Commission history
fees = client.account().get_commission_history("BTC-USDT")

# Build P&L dashboard
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

print(f"Net P&L: {stats['total_pnl']}")
print(f"Fees Paid: {stats['total_fees']}")
print(f"Funding Received: {stats['total_funding']}")
```

### 4. Multi-Assets Margin

Use your entire portfolio as collateral:

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

# Breakdown by asset
for asset in margin['assets']:
    print(f"{asset['asset']}: Balance: {asset['walletBalance']}, "
          f"Collateral: {asset['crossMarginAsset']}")

# Get multi-assets rules (haircuts, supported assets)
rules = client.trade().get_multi_assets_rules()

# Disable multi-assets mode
client.trade().switch_multi_assets_mode(False)
```

**⚠️ Warning**: In multi-assets mode, liquidation affects your entire portfolio, not just individual positions.

### 5. TWAP Orders (Time-Weighted Average Price)

Execute large orders without moving the market:

```python
# Create TWAP buy order
twap = client.twap().buy(
    symbol="BTC-USDT",
    quantity=10.0,
    duration=3600,  # Execute over 1 hour (in seconds)
    position_side="LONG"
)

print(f"TWAP Order ID: {twap['orderId']}")

# Monitor progress
import time

while True:
    details = client.twap().get_order_detail(twap['orderId'])
    
    if details['status'] == 'FILLED':
        print(f"Completed at avg price: {details['avgPrice']}")
        break
    
    progress = (float(details['executedQty']) / float(details['totalQty'])) * 100
    print(f"Progress: {progress:.2f}%")
    
    time.sleep(60)

# Create TWAP sell order
twap_sell = client.twap().sell(
    symbol="BTC-USDT",
    quantity=5.0,
    duration=1800,  # 30 minutes
    position_side="SHORT"
)

# Get all open TWAP orders
open_orders = client.twap().get_open_orders("BTC-USDT")

# Get TWAP order history
history = client.twap().get_order_history(
    symbol="BTC-USDT",
    limit=50
)

# Cancel TWAP order
client.twap().cancel_order(twap['orderId'])
```

### 6. Advanced Order Types

New order types for sophisticated trading:

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

# How it works:
# 1. Price hits $50k → Start trailing
# 2. Price climbs to $55k → Stop follows to $53.9k (2% behind)
# 3. Price rockets to $60k → Stop moves to $58.8k
# 4. Price drops to $58.8k → SOLD!

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

### 7. Auto-Add Margin

Automatic margin addition to prevent liquidation:

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
    print("Auto-add margin is ON")

# Disable auto-add margin
client.trade().set_auto_add_margin(
    symbol="BTC-USDT",
    position_side="LONG",
    enabled=False
)
```

**Note**: Only works in hedge mode. Uses your available balance.

### 8. One-Click Position Reversal

Atomically reverse your position:

```python
# Currently LONG 1.0 BTC
# This closes the long AND opens SHORT 1.0 BTC atomically
client.trade().one_click_reverse_position("BTC-USDT")

# Now you're SHORT 1.0 BTC - no gap, no slippage
```

Perfect for trend reversal strategies and "oh crap, I was wrong" moments.

## Backward Compatibility

**All your existing code continues to work.** No breaking changes.

```python
# This still works exactly as before
price = client.market().get_latest_price("BTC-USDT")
balance = client.account().get_balance()

order = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.001
})
```

## Migration Checklist

- [ ] Update package: `pip install --upgrade bingx-python`
- [ ] Test existing code (it should work unchanged)
- [ ] Try position risk monitoring
- [ ] Experiment with new order types on small positions
- [ ] Test TWAP orders with minimal amounts
- [ ] Consider multi-assets margin (only if experienced)
- [ ] Update your bots with new features when ready

## Income Types Reference

| Income Type | Description |
|-------------|-------------|
| `REALIZED_PNL` | Actual profits/losses from closed trades |
| `FUNDING_FEE` | 8-hour funding payments (can be positive or negative) |
| `COMMISSION` | Trading fees paid to BingX |
| `TRANSFER` | Money moving between accounts |
| `INSURANCE_CLEAR` | Insurance fund settlements (rare) |

## Order Types Reference

| Order Type | Description | Use Case |
|------------|-------------|----------|
| `MARKET` | Execute immediately at market price | Quick entry/exit |
| `LIMIT` | Execute at specific price or better | Price control |
| `STOP` | Trigger market order at stop price | Stop-loss |
| `STOP_LIMIT` | Trigger limit order at stop price | Stop-loss with price control |
| `TRAILING_STOP_MARKET` | Stop that follows price | Lock in profits |
| `TRIGGER_LIMIT` | Conditional limit order | Advanced entries |
| `TRAILING_TP_SL` | Trailing take profit/stop loss | Advanced exits |

## Best Practices

1. **Start Small**: Test new features with minimal amounts
2. **Monitor Risk**: Use position risk monitoring in production
3. **Track Income**: Understand where your money goes
4. **Use TWAP**: For orders > $10k to minimize slippage
5. **Be Careful**: Multi-assets margin is powerful but risky

## Support

- **Documentation**: See README.md
- **Examples**: Check examples/ directory
- **Issues**: https://github.com/tigusigalpa/bingx-python/issues
- **BingX API Docs**: https://bingx-api.github.io/docs-v3/

## License

MIT License - see LICENSE file for details.
