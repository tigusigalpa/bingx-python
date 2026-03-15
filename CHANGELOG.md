# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-03-15

### Added

#### Market Service
- **Spot Symbols Endpoint Update**: Updated `get_spot_symbols()` to use `/openApi/spot/v1/common/symbols` endpoint
  - Added support for `maxMarketNotional` field (maximum notional amount for single market order)
  - Added new symbol status value `29 = Pre-Delisted`
  - Full status values: 0=Offline, 1=Online, 5=Pre-open, 10=Accessed, 25=Suspended, 29=Pre-Delisted, 30=Delisted

- **Spot Klines v2 Endpoint**: Updated `get_spot_klines()` to use `/openApi/spot/v2/market/kline`
  - Added optional `time_zone` parameter (0=UTC (default), 8=UTC+8)
  - Updated max limit from 1000 to 1440 records

#### Spot Account Service
- **Internal Transfer Update**: Updated `internal_transfer()` method with new parameters
  - Changed `wallet_type` to integer: 1=Fund Account, 2=Standard Futures, 3=Perpetual Futures, **4=Spot Account** (NEW)
  - Added `user_account_type` parameter (1=UID, 2=Phone number, 3=Email)
  - Added `user_account` parameter
  - Added optional `calling_code` parameter (required when user_account_type=2)
  - Added optional `transfer_client_id` parameter (custom ID, max 100 chars)
  - Added optional `recv_window` parameter

#### Sub-Account Service
- **Sub-Account Internal Transfer Update**: Updated `sub_account_internal_transfer()` with new parameters
  - Changed `wallet_type` to integer: 1=Fund Account, 2=Standard Futures, 3=Perpetual Futures, **15=Spot Account** (NEW)
  - Added `user_account_type` parameter (1=UID, 2=Phone number, 3=Email)
  - Added `user_account` parameter
  - Added optional `calling_code` parameter
  - Added optional `transfer_client_id` parameter
  - Added optional `recv_window` parameter

- **New Method**: `sub_mother_account_asset_transfer()` - Sub-Mother Account Asset Transfer Interface
  - Flexible asset transfer between parent and sub-accounts
  - Supports account types: 1=Funding, 2=Standard futures, 3=Perpetual U-based, 15=Spot
  - Only available to master account
  - Returns `tranId` (transfer record ID)

- **New Method**: `get_sub_mother_account_transferable_amount()` - Query Sub-Mother Account Transferable Amount
  - Query supported coins and available transferable amounts
  - Only available to master account
  - Returns coins array with id, name, and availableAmount

- **New Method**: `get_sub_mother_account_transfer_history()` - Query Sub-Mother Account Transfer History
  - Query transfer history between sub-accounts and parent account
  - Supports filtering by type, tran_id, time range
  - Pagination support (page_id, paging_size)
  - Only available to master account

### Changed
- Updated BingX API integration to support changes from December 2025 through February 2026
- Improved parameter validation and type safety across all updated methods

### API Compatibility
- Breaking changes in method signatures for `internal_transfer()` and `sub_account_internal_transfer()`
- All new parameters are optional with sensible defaults where applicable
- Maintains Python naming conventions (snake_case)

---

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
