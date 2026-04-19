# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-27

### 🔴 Critical Fixes

#### BaseHTTPClient
- Added `X-SOURCE-KEY: BX-AI-SKILL` header by default (required by BingX API)
- Changed default signature encoding from `base64` to `hex`
- Implemented automatic fallback to `.pro` domain on network/timeout errors
- Added JSON body support for Sub-Account API endpoints (`body_type="json"`)
- Fixed `_handle_api_error()` to not throw exception on success (`code === 0`)

#### Coin-M Futures
- `get_commission_rate()` → `/openApi/cswap/v1/user/commissionRate`
- `get_positions()` → `/openApi/cswap/v1/user/positions`
- `get_balance()` → `/openApi/cswap/v1/user/balance`
- `cancel_order()` → `/openApi/cswap/v1/trade/cancelOrder`
- `get_order()` → `/openApi/cswap/v1/trade/orderDetail`
- `cancel_all_orders()` → Changed from DELETE to POST
- `get_funding_rate()` → `/openApi/cswap/v1/market/premiumIndex`
- Added `get_mark_price()`, `get_recent_trades()`, `get_latest_price()`, `get_book_ticker()`
- Added `close_all_positions()`, `get_leverage()`, `get_margin_type()`
- Listen Key endpoints now use `/openApi/user/auth/userDataStream`

### 🔧 USDT-M Endpoint Updates

#### AccountService
- `get_balance()` → Updated to v3 API `/openApi/swap/v3/user/balance`

#### MarketService
- `get_klines()` → `/openApi/swap/v3/quote/klines`
- `get_depth()` → `/openApi/swap/v2/quote/depth`
- `get_recent_trades()` → `/openApi/swap/v2/quote/trades`
- `get_mark_price()` → `/openApi/swap/v2/quote/premiumIndex`
- `get_24hr_ticker()` → `/openApi/swap/v2/quote/ticker`
- `get_quote_funding_rate()` → Now accepts optional symbol parameter

### 🔄 Sub-Account API Updates

Methods now use JSON body as required:
- `create_sub_account()` - added optional `note` parameter
- `create_sub_account_api_key()` - updated to use `sub_uid`, `permissions` array, `ip_addresses` list
- `edit_sub_account_api_key()` - updated to use `sub_uid`, `ip_addresses` list
- `delete_sub_account_api_key()` - updated to use `sub_uid`
- `query_api_key()` - updated to use `sub_uid`
- `update_sub_account_status()` - changed to `sub_uid` and `freeze: bool` parameters

### ✨ New Services

#### AgentService (affiliate/broker data)
- `get_invited_users()` - Query invited users (paginated)
- `get_daily_commission()` - Daily commission details (invitation relationship)
- `get_user_info()` - Query agent user information for a UID
- `get_api_commission()` - API transaction commission (non-invitation relationship)
- `get_partner_info()` - Query partner information
- `get_deposit_details()` - Query deposit details of invited users
- `get_referral_code_commission()` - Query invitation code commission data
- `check_superior_agent()` - Check if a user is a superior agent

#### AnnouncementService (public announcements)
- `get_announcements()` - Get announcements by module type
- `get_latest_announcements()` - Get latest announcements
- `get_promotions()` - Get latest promotions
- `get_product_updates()` - Get product updates
- `get_maintenance_notices()` - Get system maintenance notices
- `get_asset_maintenance()` - Get asset maintenance notices
- `get_spot_listings()` - Get spot new listings
- `get_futures_listings()` - Get futures new listings
- `get_delistings()` - Get delisting notices
- `get_funding_rate_notices()` - Get funding rate notices
- `get_crypto_scout()` - Get crypto scout announcements

### ⚠️ Breaking Changes

- `SubAccountService.update_sub_account_status()` signature changed from `(sub_account_string: str, status: int)` to `(sub_uid: str, freeze: bool)`
- `SubAccountService.create_sub_account_api_key()` parameter names changed: `sub_account_string` → `sub_uid`, `label` → `note`, `permissions` now `List[str]`, `ip` → `ip_addresses: List[str]`
- `SubAccountService.edit_sub_account_api_key()` parameter names changed: `sub_account_string` → `sub_uid`, `ip` → `ip_addresses: List[str]`
- `SubAccountService.delete_sub_account_api_key()` parameter changed: `sub_account_string` → `sub_uid`
- `SubAccountService.query_api_key()` parameter changed: `sub_account_string` → `sub_uid`
- Default signature encoding changed from `base64` to `hex`

---

## [Unreleased] - 2026-04-05

### Added - API v3 Support

#### New TWAP Service
- **TWAPService**: Time-Weighted Average Price order execution for minimizing market impact
  - `buy()` - Create TWAP buy order with duration and optional price limit
  - `sell()` - Create TWAP sell order with duration and optional price limit
  - `get_order_detail()` - Get TWAP order execution progress and details
  - `get_open_orders()` - Get all open TWAP orders
  - `get_order_history()` - Get historical TWAP orders
  - `cancel_order()` - Cancel a TWAP order
  - `cancel_all_orders()` - Cancel all TWAP orders for a symbol

#### Market Service - API v3 Endpoints
- `get_open_interest()` - Get current open interest for a symbol
- `get_open_interest_history()` - Get historical open interest data with configurable periods (5m, 15m, 30m, 1h, 4h, 1d)
- `get_funding_rate_info()` - Get current funding rate and next funding time
- `get_index_price()` - Get index price for a symbol

#### Account Service - API v3 Endpoints
- `get_position_risk()` - Get detailed position risk metrics including:
  - Liquidation price
  - Margin ratio
  - Unrealized P&L
  - Entry price and mark price
- `get_income_history()` - Get income history with filtering by type:
  - REALIZED_PNL - Actual profits/losses from closed trades
  - FUNDING_FEE - 8-hour funding payments
  - COMMISSION - Trading fees
  - TRANSFER - Account transfers
  - INSURANCE_CLEAR - Insurance fund settlements
- `get_commission_history()` - Get detailed commission history

#### Trade Service - API v3 Features
- **Multi-Assets Margin Mode**:
  - `switch_multi_assets_mode()` - Enable/disable portfolio-wide margin
  - `get_multi_assets_mode()` - Get current multi-assets margin status
  - `get_multi_assets_margin()` - Get margin info including total collateral, margin used, available margin
  - `get_multi_assets_rules()` - Get supported assets and haircut rates
- **Auto-Add Margin**:
  - `set_auto_add_margin()` - Enable/disable automatic margin addition to prevent liquidation
  - `get_auto_add_margin()` - Get auto-add margin status
- **Position Management**:
  - `one_click_reverse_position()` - Atomically reverse position (LONG → SHORT or SHORT → LONG)

#### New Order Types Support
- `TRAILING_STOP_MARKET` - Stop-loss that follows price to lock in profits
- `TRIGGER_LIMIT` - Conditional limit order triggered at specific price
- `TRAILING_TP_SL` - Trailing take profit and stop loss

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
