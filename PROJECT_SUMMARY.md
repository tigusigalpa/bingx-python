# BingX Python SDK - Project Summary

## Overview

A comprehensive Python client library for the BingX cryptocurrency exchange API, based on the existing PHP and Go implementations. This library provides full support for USDT-M and Coin-M perpetual futures, spot trading, copy trading, sub-accounts, and WebSocket streaming.

## Project Information

- **Package Name**: bingx-python
- **GitHub Repository**: https://github.com/tigusigalpa/bingx-python
- **Author**: Igor Sazonov (sovletig@gmail.com)
- **License**: MIT
- **Python Version**: 3.8+

## Project Structure

```
bingx-python/
├── bingx/                          # Main package
│   ├── __init__.py                 # Package initialization
│   ├── client.py                   # Main BingX client
│   ├── coinm_client.py             # Coin-M futures client
│   ├── exceptions.py               # Custom exceptions
│   ├── http/                       # HTTP client module
│   │   ├── __init__.py
│   │   └── base_client.py          # Base HTTP client with HMAC-SHA256 signing
│   ├── services/                   # API service modules
│   │   ├── __init__.py
│   │   ├── account.py              # Account operations
│   │   ├── contract.py             # Standard contracts
│   │   ├── copy_trading.py         # Copy trading
│   │   ├── listen_key.py           # WebSocket authentication
│   │   ├── market.py               # Market data (40+ methods)
│   │   ├── spot_account.py         # Spot account operations
│   │   ├── sub_account.py          # Sub-account management
│   │   ├── trade.py                # Trading operations
│   │   ├── wallet.py               # Wallet operations
│   │   └── coinm/                  # Coin-M specific services
│   │       ├── __init__.py
│   │       ├── listen_key.py
│   │       ├── market.py
│   │       └── trade.py
│   └── websocket/                  # WebSocket clients
│       ├── __init__.py
│       ├── account_data_stream.py  # Private data stream
│       └── market_data_stream.py   # Public data stream
├── examples/                       # Usage examples
│   ├── basic_usage.py
│   ├── coinm_example.py
│   ├── trading_example.py
│   └── websocket_example.py
├── tests/                          # Unit tests
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_exceptions.py
│   └── test_http_client.py
├── .github/workflows/              # GitHub Actions
│   └── python-package.yml
├── .flake8                         # Flake8 configuration
├── .gitignore                      # Git ignore file
├── CHANGELOG.md                    # Version history
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # MIT License
├── MANIFEST.in                     # Package manifest
├── README.md                       # Main documentation
├── pyproject.toml                  # Modern Python packaging
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
└── setup.py                        # Setup script
```

## Key Features

### 1. **Comprehensive API Coverage**
- **Market Service**: 40+ methods for market data, Quote API, symbols, prices, candles
- **Account Service**: 25+ methods for balance, positions, leverage, margin management
- **Trade Service**: 30+ methods for orders, trade history, position management
- **Wallet Service**: Deposits, withdrawals, wallet addresses
- **Spot Account Service**: Spot balance, transfers, internal transfers
- **Sub-Account Service**: 20+ methods for sub-account management
- **Copy Trading Service**: 13+ methods for copy trading operations
- **Contract Service**: Standard contract API
- **Coin-M Services**: Full support for crypto-margined contracts

### 2. **Security Features**
- HMAC-SHA256 signature for all authenticated requests
- Automatic timestamp validation
- Support for both base64 and hex signature encoding
- Replay attack protection with recvWindow parameter
- Custom exception classes for different error types

### 3. **WebSocket Support**
- **MarketDataStream**: Real-time public market data
  - Trade streams
  - Kline/candlestick streams
  - Depth/order book streams
  - 24hr ticker streams
  - Best bid/ask streams
- **AccountDataStream**: Real-time private account data
  - Balance updates
  - Position updates
  - Order updates

### 4. **Developer Experience**
- Type hints for better IDE support
- Comprehensive error handling with custom exceptions
- Clean and intuitive API design
- Extensive documentation and examples
- Unit tests with pytest
- Code formatting with Black
- Linting with flake8
- Type checking with mypy

## Installation

```bash
# From PyPI (when published)
pip install bingx-python

# From source
git clone https://github.com/tigusigalpa/bingx-python.git
cd bingx-python
pip install -e .
```

## Quick Start

```python
from bingx import BingXClient

# Initialize client
client = BingXClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Get current price
price = client.market().get_latest_price("BTC-USDT")

# Get account balance
balance = client.account().get_balance()

# Create order
order = client.trade().create_order({
    "symbol": "BTC-USDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.001
})
```

## API Services

### Market Service
- Futures and spot symbols
- Latest prices and 24hr tickers
- Market depth (order book)
- Candlestick data (klines)
- Funding rates and mark prices
- Aggregate trades and recent trades
- Long/short ratios
- Contract basis data
- Quote API for optimized data

### Account Service
- Account balance and positions
- Leverage management
- Margin mode (ISOLATED/CROSSED)
- Position margin adjustment
- Trading fees and commission rates
- API permissions and rate limits
- Balance and deposit/withdrawal history
- Asset management

### Trade Service
- Create, cancel, and manage orders
- Batch order operations
- Test orders (no execution)
- Order history and trade history
- Quick trade methods (spot/futures)
- Position management
- Commission calculations
- Margin type management

### Wallet Service
- Deposit history and addresses
- Withdrawal history and creation
- Coin information

### Spot Account Service
- Spot and fund balances
- Universal transfers
- Asset transfer records
- Internal transfers (main ↔ sub)
- All account balances

### Sub-Account Service
- Create and manage sub-accounts
- API key management for sub-accounts
- Internal transfers between accounts
- Asset transfers
- Deposit address management
- Deposit history

### Copy Trading Service
- Track orders (futures and spot)
- Close positions
- Set take profit/stop loss
- Trader details and profit summary
- Commission management
- Trading pairs

### Coin-M Services
- Market data for crypto-margined contracts
- Trading operations
- Position and balance management
- Leverage and margin settings

## WebSocket Streaming

### Market Data Stream
```python
from bingx.websocket import MarketDataStream

stream = MarketDataStream()
stream.connect()
stream.subscribe_trade("BTC-USDT")
stream.subscribe_kline("BTC-USDT", "1m")
stream.on_message(lambda data: print(data))
stream.listen_async()
```

### Account Data Stream
```python
from bingx.websocket import AccountDataStream

listen_key = client.listen_key().generate()["listenKey"]
stream = AccountDataStream(listen_key)
stream.connect()
stream.on_balance_update(lambda balances: print(balances))
stream.on_order_update(lambda order: print(order))
stream.listen_async()
```

## Error Handling

Custom exception hierarchy:
- `BingXException` - Base exception
- `APIException` - API-level errors
- `AuthenticationException` - Invalid credentials
- `RateLimitException` - Rate limit exceeded
- `InsufficientBalanceException` - Insufficient balance

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=bingx --cov-report=html

# Run specific test
pytest tests/test_client.py -v
```

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Format code
black bingx/

# Lint code
flake8 bingx/

# Type check
mypy bingx --ignore-missing-imports
```

## Dependencies

### Production
- `requests>=2.31.0` - HTTP client
- `websocket-client>=1.6.0` - WebSocket support

### Development
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.7.0` - Code formatting
- `flake8>=6.1.0` - Linting
- `mypy>=1.5.0` - Type checking

## Comparison with Other Libraries

### vs PHP Library
- Similar structure and API design
- Python-specific features (type hints, async support)
- More Pythonic naming conventions
- Better exception handling

### vs Go Library
- Similar architecture
- Python's dynamic typing vs Go's static typing
- More flexible error handling
- Easier to use for rapid development

## Future Enhancements

Potential improvements:
- Async/await support with aiohttp
- Rate limiting middleware
- Automatic retry logic
- Response caching
- More comprehensive test coverage
- Integration tests
- Performance optimizations
- Additional utility functions

## Publishing to PyPI

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

## Support and Resources

- **Documentation**: See README.md
- **Examples**: See examples/ directory
- **Issues**: https://github.com/tigusigalpa/bingx-python/issues
- **BingX API Docs**: https://bingx-api.github.io/docs/

## License

MIT License - see LICENSE file for details.

## Author

Igor Sazonov (sovletig@gmail.com)
GitHub: @tigusigalpa
