"""
BingX Python SDK - API v3 Examples

Demonstrates new features introduced in API v3:
- TWAP orders for large trades
- Position risk monitoring
- Income and commission tracking
- Multi-assets margin mode
- Auto-add margin
- One-click position reversal
- Enhanced market data
"""

import time
from bingx import BingXClient

# Initialize client
client = BingXClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)


# ============================================================================
# TWAP ORDERS - Execute large orders without moving the market
# ============================================================================

def twap_order_example():
    """Execute a large order using TWAP to minimize market impact"""
    
    # Create TWAP buy order - execute 10 BTC over 1 hour
    twap = client.twap().buy(
        symbol="BTC-USDT",
        quantity=10.0,
        duration=3600,  # 1 hour in seconds
        position_side="LONG"
    )
    
    print(f"TWAP Order Created: {twap['orderId']}")
    
    # Monitor progress
    while True:
        details = client.twap().get_order_detail(twap['orderId'])
        
        if details['status'] == 'FILLED':
            print(f"✅ Completed at avg price: {details['avgPrice']}")
            break
        
        executed = float(details['executedQty'])
        total = float(details['totalQty'])
        progress = (executed / total) * 100
        
        print(f"Progress: {progress:.2f}% ({executed}/{total} BTC)")
        time.sleep(60)  # Check every minute
    
    # Create TWAP sell order with price limit
    twap_sell = client.twap().sell(
        symbol="BTC-USDT",
        quantity=5.0,
        duration=1800,  # 30 minutes
        position_side="SHORT",
        price_limit=60000  # Won't execute below $60k
    )
    
    # Get all open TWAP orders
    open_orders = client.twap().get_open_orders("BTC-USDT")
    print(f"Open TWAP orders: {len(open_orders)}")
    
    # Cancel TWAP order if needed
    # client.twap().cancel_order(twap['orderId'])


# ============================================================================
# POSITION RISK MONITORING - Know before you blow
# ============================================================================

def position_risk_monitoring():
    """Monitor position risk in real-time to prevent liquidation"""
    
    # Get position risk for a symbol
    risk = client.account().get_position_risk("BTC-USDT")
    
    print(f"Position Size: {risk['positionAmt']}")
    print(f"Entry Price: {risk['entryPrice']}")
    print(f"Mark Price: {risk['markPrice']}")
    print(f"Liquidation Price: {risk['liquidationPrice']}")
    print(f"Margin Ratio: {risk['marginRatio']}%")
    print(f"Unrealized P&L: {risk['unrealizedProfit']}")
    
    # Real-time risk monitoring loop
    def monitor_risk():
        while True:
            risk = client.account().get_position_risk("BTC-USDT")
            margin_ratio = float(risk['marginRatio'])
            
            if margin_ratio > 80:
                print(f"🚨 CRITICAL: Margin at {margin_ratio}%!")
                # Take action: add margin, close positions, etc.
                send_alert(f"High risk position! Margin ratio: {margin_ratio}%")
            elif margin_ratio > 60:
                print(f"⚠️ WARNING: Margin at {margin_ratio}%")
            else:
                print(f"✅ Safe: Margin at {margin_ratio}%")
            
            time.sleep(60)  # Check every minute


# ============================================================================
# INCOME & COMMISSION TRACKING - Where did my money go?
# ============================================================================

def income_tracking_example():
    """Track all income types to understand P&L"""
    
    # Get all income history
    income = client.account().get_income_history(
        symbol="BTC-USDT",
        limit=100
    )
    
    # Filter by income type
    pnl = client.account().get_income_history(
        symbol="BTC-USDT",
        income_type="REALIZED_PNL"
    )
    
    funding = client.account().get_income_history(
        symbol="BTC-USDT",
        income_type="FUNDING_FEE"
    )
    
    # Get commission history
    fees = client.account().get_commission_history("BTC-USDT")
    
    # Build P&L dashboard
    stats = {
        'total_pnl': 0,
        'total_fees': 0,
        'total_funding': 0,
    }
    
    for record in income:
        income_value = float(record['income'])
        
        if record['incomeType'] == 'REALIZED_PNL':
            stats['total_pnl'] += income_value
        elif record['incomeType'] == 'COMMISSION':
            stats['total_fees'] += income_value
        elif record['incomeType'] == 'FUNDING_FEE':
            stats['total_funding'] += income_value
    
    print(f"Net P&L: ${stats['total_pnl']:.2f}")
    print(f"Fees Paid: ${abs(stats['total_fees']):.2f}")
    print(f"Funding Received: ${stats['total_funding']:.2f}")
    print(f"True Profit: ${stats['total_pnl'] + stats['total_fees'] + stats['total_funding']:.2f}")


# ============================================================================
# MULTI-ASSETS MARGIN - Your whole portfolio works for you
# ============================================================================

def multi_assets_margin_example():
    """Use entire portfolio as collateral"""
    
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
    print("\nAsset Breakdown:")
    for asset in margin['assets']:
        print(f"{asset['asset']}: "
              f"Balance: {asset['walletBalance']}, "
              f"Collateral: {asset['crossMarginAsset']}")
    
    # Get multi-assets rules (haircuts, supported assets)
    rules = client.trade().get_multi_assets_rules()
    print("\nSupported Assets:")
    for rule in rules:
        print(f"{rule['asset']}: Haircut {rule['haircut']}%")
    
    # Disable multi-assets mode (only when no positions)
    # client.trade().switch_multi_assets_mode(False)


# ============================================================================
# AUTO-ADD MARGIN - Your safety net
# ============================================================================

def auto_add_margin_example():
    """Automatically add margin to prevent liquidation"""
    
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
    else:
        print("❌ Auto-add margin is OFF")
    
    # Disable auto-add margin
    # client.trade().set_auto_add_margin(
    #     symbol="BTC-USDT",
    #     position_side="LONG",
    #     enabled=False
    # )


# ============================================================================
# ONE-CLICK POSITION REVERSAL - Change your mind instantly
# ============================================================================

def one_click_reverse_example():
    """Atomically reverse position direction"""
    
    # Currently LONG 1.0 BTC
    # This closes the long AND opens SHORT 1.0 BTC atomically
    result = client.trade().one_click_reverse_position("BTC-USDT")
    
    print("Position reversed!")
    print(f"New position: {result}")
    
    # Now you're SHORT 1.0 BTC - no gap, no slippage


# ============================================================================
# ENHANCED MARKET DATA - See what the pros see
# ============================================================================

def enhanced_market_data_example():
    """Access institutional-grade market data"""
    
    # Open Interest - how much is currently open
    oi = client.market().get_open_interest("BTC-USDT")
    print(f"Open Interest: {oi['openInterest']}")
    
    # Historical OI with different periods
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


# ============================================================================
# ADVANCED ORDER TYPES - New order types for sophisticated trading
# ============================================================================

def advanced_order_types_example():
    """Use new order types introduced in API v3"""
    
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


# ============================================================================
# COMPLETE TRADING BOT WITH API v3 FEATURES
# ============================================================================

def advanced_trading_bot():
    """Complete trading bot using API v3 features"""
    
    symbol = "BTC-USDT"
    
    while True:
        try:
            # 1. Check position risk
            risk = client.account().get_position_risk(symbol)
            
            if risk and float(risk['marginRatio']) > 80:
                print("🚨 High risk! Skipping trade")
                time.sleep(60)
                continue
            
            # 2. Get enhanced market data
            price = client.market().get_latest_price(symbol)
            oi = client.market().get_open_interest(symbol)
            funding = client.market().get_funding_rate_info(symbol)
            
            current_price = float(price['price'])
            funding_rate = float(funding['fundingRate'])
            
            print(f"Price: ${current_price}, Funding: {funding_rate}%")
            
            # 3. Trading logic
            if current_price < 48000 and funding_rate < 0.01:
                # Use TWAP for large orders
                if should_use_twap(quantity=10.0):
                    twap = client.twap().buy(
                        symbol=symbol,
                        quantity=10.0,
                        duration=3600,
                        position_side="LONG"
                    )
                    print(f"TWAP order created: {twap['orderId']}")
                else:
                    # Regular order with trailing stop
                    order = client.trade().create_order({
                        "symbol": symbol,
                        "side": "BUY",
                        "positionSide": "LONG",
                        "type": "MARKET",
                        "quantity": 1.0
                    })
                    
                    # Set trailing stop
                    client.trade().create_order({
                        "symbol": symbol,
                        "side": "SELL",
                        "positionSide": "LONG",
                        "type": "TRAILING_STOP_MARKET",
                        "quantity": 1.0,
                        "activationPrice": 50000,
                        "callbackRate": 2.0
                    })
            
            # 4. Monitor income
            income = client.account().get_income_history(
                symbol=symbol,
                limit=10
            )
            
            total_pnl = sum(float(i['income']) for i in income 
                          if i['incomeType'] == 'REALIZED_PNL')
            print(f"Recent P&L: ${total_pnl:.2f}")
            
            time.sleep(60)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)


def should_use_twap(quantity: float) -> bool:
    """Determine if order is large enough to warrant TWAP"""
    # Use TWAP for orders > $100k notional
    return quantity > 2.0  # Adjust based on your needs


def send_alert(message: str):
    """Send alert (implement your notification method)"""
    print(f"ALERT: {message}")
    # Implement: email, SMS, Telegram, etc.


# ============================================================================
# RUN EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("BingX API v3 Examples")
    print("=" * 50)
    
    # Uncomment to run specific examples:
    
    # twap_order_example()
    # position_risk_monitoring()
    # income_tracking_example()
    # multi_assets_margin_example()
    # auto_add_margin_example()
    # one_click_reverse_example()
    # enhanced_market_data_example()
    # advanced_order_types_example()
    # advanced_trading_bot()
    
    print("\nExamples completed!")
