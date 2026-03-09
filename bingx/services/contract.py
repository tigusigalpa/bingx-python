"""
Contract Service

Handles standard contract operations.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class ContractService:
    """Service for standard contract operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Contract Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_all_positions(
        self, timestamp: Optional[int] = None, recv_window: int = 5000
    ) -> Dict[str, Any]:
        """
        Get all positions for standard contracts

        Args:
            timestamp: Timestamp in milliseconds
            recv_window: Receive window in milliseconds
        """
        params = {"recvWindow": recv_window}
        if timestamp:
            params["timestamp"] = timestamp
        return self.client.request("GET", "/openApi/contract/v1/allPosition", params)

    def get_all_orders(
        self,
        symbol: str,
        limit: int = 100,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get historical orders for a specific symbol

        Args:
            symbol: Trading symbol
            limit: Number of orders
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
        """
        params = {"symbol": symbol, "limit": limit}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/contract/v1/allOrders", params)

    def get_balance(self) -> Dict[str, Any]:
        """Query standard contract account balance"""
        return self.client.request("GET", "/openApi/contract/v1/balance")
