"""
Market Service

Handles market data operations including prices, depth, klines, funding rates, etc.
"""

from typing import Any, Dict, List, Optional

from ..http.base_client import BaseHTTPClient


class MarketService:
    """Service for market data operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Market Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_futures_symbols(self) -> Dict[str, Any]:
        """Get futures/swap contract symbols"""
        return self.client.request("GET", "/openApi/swap/v2/market/symbols")

    def get_spot_symbols(self) -> Dict[str, Any]:
        """
        Get spot trading symbols
        
        Response includes:
        - maxMarketNotional: Maximum notional amount for a single market order
        - status: Symbol status (0=Offline, 1=Online, 5=Pre-open, 10=Accessed, 
                  25=Suspended, 29=Pre-Delisted, 30=Delisted)
        """
        return self.client.request("GET", "/openApi/spot/v1/common/symbols")

    def get_all_symbols(self) -> Dict[str, Any]:
        """Get all available symbols (both spot and futures)"""
        return {"spot": self.get_spot_symbols(), "futures": self.get_futures_symbols()}

    def get_symbols(self) -> Dict[str, Any]:
        """Get contract symbols (alias for get_futures_symbols)"""
        return self.get_futures_symbols()

    def get_latest_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get latest price for a futures symbol

        Args:
            symbol: Trading symbol (e.g., "BTC-USDT")
        """
        return self.client.request("GET", "/openApi/swap/v2/market/latestPrice", {"symbol": symbol})

    def get_spot_latest_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get latest price for a spot symbol

        Args:
            symbol: Trading symbol (e.g., "BTC-USDT")
        """
        return self.client.request("GET", "/openApi/spot/v1/market/ticker/price", {"symbol": symbol})

    def get_depth(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get market depth (order book) for futures

        Args:
            symbol: Trading symbol
            limit: Number of depth levels (5, 10, 20)
        """
        return self.client.request("GET", "/openApi/swap/v2/market/depth", {"symbol": symbol, "limit": limit})

    def get_spot_depth(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get market depth (order book) for spot

        Args:
            symbol: Trading symbol
            limit: Number of depth levels (5, 10, 20)
        """
        return self.client.request("GET", "/openApi/spot/v1/market/depth", {"symbol": symbol, "limit": limit})

    def get_klines(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get candlestick data for futures

        Args:
            symbol: Trading symbol
            interval: Kline interval (1m, 5m, 15m, 30m, 1h, 4h, 1d, etc.)
            limit: Number of klines to return
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
        """
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/swap/v2/market/klines", params)

    def get_spot_klines(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        time_zone: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get candlestick data for spot

        Args:
            symbol: Trading symbol
            interval: Kline interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
            limit: Number of klines to return (max 1440)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            time_zone: Timezone offset (0=UTC (default), 8=UTC+8)
        """
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if time_zone is not None:
            params["timeZone"] = time_zone
        return self.client.request("GET", "/openApi/spot/v2/market/kline", params)

    def get_24hr_ticker(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get 24hr ticker statistics for futures

        Args:
            symbol: Trading symbol (optional, returns all if not specified)
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/swap/v2/market/ticker", params)

    def get_spot_24hr_ticker(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get 24hr ticker statistics for spot

        Args:
            symbol: Trading symbol (optional, returns all if not specified)
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/spot/v1/market/ticker/24hr", params)

    def get_funding_rate_history(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get funding rate history

        Args:
            symbol: Trading symbol
            limit: Number of records to return
        """
        return self.client.request("GET", "/openApi/swap/v2/market/fundingRate", {"symbol": symbol, "limit": limit})

    def get_mark_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get mark price

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/market/markPrice", {"symbol": symbol})

    def get_premium_index_klines(
        self, symbol: str, interval: str, limit: int = 500
    ) -> Dict[str, Any]:
        """
        Get premium index klines

        Args:
            symbol: Trading symbol
            interval: Kline interval
            limit: Number of klines
        """
        return self.client.request(
            "GET",
            "/openApi/swap/v2/market/premiumIndexKlines",
            {"symbol": symbol, "interval": interval, "limit": limit},
        )

    def get_continuous_klines(
        self, symbol: str, interval: str, limit: int = 500
    ) -> Dict[str, Any]:
        """
        Get continuous contract klines

        Args:
            symbol: Trading symbol
            interval: Kline interval
            limit: Number of klines
        """
        return self.client.request(
            "GET",
            "/openApi/swap/v2/market/continuousKlines",
            {"symbol": symbol, "interval": interval, "limit": limit},
        )

    def get_aggregate_trades(self, symbol: str, limit: int = 500) -> Dict[str, Any]:
        """
        Get aggregate trades for futures

        Args:
            symbol: Trading symbol
            limit: Number of trades
        """
        return self.client.request("GET", "/openApi/swap/v2/market/aggTrades", {"symbol": symbol, "limit": limit})

    def get_recent_trades(self, symbol: str, limit: int = 500) -> Dict[str, Any]:
        """
        Get recent trades for futures

        Args:
            symbol: Trading symbol
            limit: Number of trades
        """
        return self.client.request("GET", "/openApi/swap/v2/market/trades", {"symbol": symbol, "limit": limit})

    def get_spot_aggregate_trades(self, symbol: str, limit: int = 500) -> Dict[str, Any]:
        """
        Get aggregate trades for spot

        Args:
            symbol: Trading symbol
            limit: Number of trades
        """
        return self.client.request("GET", "/openApi/spot/v1/market/aggTrades", {"symbol": symbol, "limit": limit})

    def get_spot_recent_trades(self, symbol: str, limit: int = 500) -> Dict[str, Any]:
        """
        Get recent trades for spot

        Args:
            symbol: Trading symbol
            limit: Number of trades
        """
        return self.client.request("GET", "/openApi/spot/v1/market/trades", {"symbol": symbol, "limit": limit})

    def get_top_long_short_ratio(self, symbol: str, period: int = 10) -> Dict[str, Any]:
        """
        Get top trader long/short ratio

        Args:
            symbol: Trading symbol
            period: Period in minutes
        """
        return self.client.request(
            "GET",
            "/openApi/swap/v2/market/topLongShortRatio",
            {"symbol": symbol, "period": period},
        )

    def get_historical_top_long_short_ratio(
        self,
        symbol: str,
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get historical top trader long/short ratio

        Args:
            symbol: Trading symbol
            limit: Number of records
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
        """
        params = {"symbol": symbol, "limit": limit}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/swap/v2/market/historicalTopLongShortRatio", params)

    def get_basis(self, symbol: str, contract_type: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get contract basis data

        Args:
            symbol: Trading symbol
            contract_type: Contract type (e.g., 'PERPETUAL')
            limit: Number of records
        """
        return self.client.request(
            "GET",
            "/openApi/swap/v2/market/basis",
            {"symbol": symbol, "contractType": contract_type, "limit": limit},
        )

    def get_contracts(self) -> Dict[str, Any]:
        """Get all contract specifications (Quote API)"""
        return self.client.request("GET", "/openApi/swap/v2/quote/contracts")

    def get_quote_depth(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get order book via Quote API (optimized)

        Args:
            symbol: Trading symbol
            limit: Number of depth levels
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/depth", {"symbol": symbol, "limit": limit})

    def get_book_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Get best bid/ask prices

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/bookTicker", {"symbol": symbol})

    def get_quote_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Get 24hr ticker via Quote API

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/ticker", {"symbol": symbol})

    def get_quote_funding_rate(self, symbol: str) -> Dict[str, Any]:
        """
        Get funding rate via Quote API

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/fundingRate", {"symbol": symbol})

    def get_quote_open_interest(self, symbol: str) -> Dict[str, Any]:
        """
        Get open interest via Quote API

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/openInterest", {"symbol": symbol})

    def get_premium_index(self, symbol: str) -> Dict[str, Any]:
        """
        Get premium index

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/premiumIndex", {"symbol": symbol})

    def get_quote_trades(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get recent trades via Quote API

        Args:
            symbol: Trading symbol
            limit: Number of trades
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/trades", {"symbol": symbol, "limit": limit})

    def get_klines_v3(self, symbol: str, interval: str, limit: int = 500) -> Dict[str, Any]:
        """
        Get K-lines v3 (improved performance)

        Args:
            symbol: Trading symbol
            interval: Kline interval
            limit: Number of klines
        """
        return self.client.request(
            "GET",
            "/openApi/swap/v3/quote/klines",
            {"symbol": symbol, "interval": interval, "limit": limit},
        )

    def get_trading_rules(self, symbol: str) -> Dict[str, Any]:
        """
        Get trading rules for a symbol

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/quote/tradingRules", {"symbol": symbol})
