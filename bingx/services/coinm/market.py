"""
Coin-M Market Service

Handles Coin-M perpetual futures market data.
"""

from typing import Any, Dict, Optional

from ...http.base_client import BaseHTTPClient


class CoinMMarketService:
    """Service for Coin-M market data operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Coin-M Market Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_contracts(self) -> Dict[str, Any]:
        """Get all Coin-M contract information"""
        return self.client.request("GET", "/openApi/cswap/v1/market/contracts")

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Get 24hr ticker for Coin-M contract

        Args:
            symbol: Trading symbol (e.g., 'BTC-USD')
        """
        return self.client.request("GET", "/openApi/cswap/v1/market/ticker", {"symbol": symbol})

    def get_depth(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get order book depth for Coin-M contract

        Args:
            symbol: Trading symbol
            limit: Depth limit
        """
        return self.client.request(
            "GET", "/openApi/cswap/v1/market/depth", {"symbol": symbol, "limit": limit}
        )

    def get_klines(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get candlestick data for Coin-M contract

        Args:
            symbol: Trading symbol
            interval: Kline interval (1m, 5m, 15m, 30m, 1h, 4h, 1d, etc.)
            limit: Number of klines
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
        """
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/cswap/v1/market/klines", params)

    def get_open_interest(self, symbol: str) -> Dict[str, Any]:
        """
        Get open interest for Coin-M contract

        Args:
            symbol: Trading symbol
        """
        return self.client.request(
            "GET", "/openApi/cswap/v1/market/openInterest", {"symbol": symbol}
        )

    def get_funding_rate(self, symbol: str) -> Dict[str, Any]:
        """
        Get funding rate for Coin-M contract

        Args:
            symbol: Trading symbol
        """
        return self.client.request(
            "GET", "/openApi/cswap/v1/market/fundingRate", {"symbol": symbol}
        )
