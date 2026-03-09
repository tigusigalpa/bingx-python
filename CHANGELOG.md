# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-03-09

### Added
- Initial release of BingX Python SDK
- Support for USDT-M Perpetual Futures
- Support for Coin-M Perpetual Futures
- Market Service with 40+ methods
- Account Service with 25+ methods
- Trade Service with 30+ methods
- Wallet Service for deposits and withdrawals
- Spot Account Service for spot trading
- Sub-Account Service for sub-account management
- Copy Trading Service for copy trading operations
- Contract Service for standard contracts
- Listen Key Service for WebSocket authentication
- WebSocket support for market data streams
- WebSocket support for account data streams
- HMAC-SHA256 signature authentication
- Support for base64 and hex signature encoding
- Custom exception classes for error handling
- Type hints for better IDE support
- Comprehensive documentation and examples

### Features
- Market data: symbols, prices, depth, klines, funding rates
- Account management: balance, positions, leverage, margin
- Trading: create/cancel orders, order history, batch operations
- Wallet operations: deposits, withdrawals, addresses
- Sub-account management: create, API keys, transfers
- Copy trading: track orders, profit summary, commission
- WebSocket: real-time market data and account updates
- Coin-M futures: crypto-margined contracts

### Security
- HMAC-SHA256 request signing
- Automatic timestamp validation
- Replay attack protection with recvWindow
- Secure API key handling

[1.0.0]: https://github.com/tigusigalpa/bingx-python/releases/tag/v1.0.0
