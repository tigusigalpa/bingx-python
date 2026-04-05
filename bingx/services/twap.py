"""
TWAP Service

Handles Time-Weighted Average Price (TWAP) order execution.
TWAP orders break large trades into smaller pieces executed over time to minimize market impact.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class TWAPService:
    """Service for TWAP (Time-Weighted Average Price) order operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize TWAP Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def buy(
        self,
        symbol: str,
        quantity: float,
        duration: int,
        position_side: str = "LONG",
        price_limit: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Create TWAP buy order

        Args:
            symbol: Trading symbol (e.g., "BTC-USDT")
            quantity: Total quantity to buy
            duration: Execution duration in seconds
            position_side: Position side (LONG or SHORT)
            price_limit: Optional price limit (won't execute above this price)

        Returns:
            TWAP order details including order ID

        Example:
            # Execute 10 BTC over 1 hour
            twap = client.twap().buy(
                symbol="BTC-USDT",
                quantity=10.0,
                duration=3600,
                position_side="LONG"
            )
        """
        params = {
            "symbol": symbol,
            "side": "BUY",
            "positionSide": position_side,
            "quantity": quantity,
            "duration": duration,
        }
        if price_limit:
            params["priceLimit"] = price_limit

        return self.client.request("POST", "/openApi/swap/v2/trade/twapOrder", params)

    def sell(
        self,
        symbol: str,
        quantity: float,
        duration: int,
        position_side: str = "SHORT",
        price_limit: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Create TWAP sell order

        Args:
            symbol: Trading symbol (e.g., "BTC-USDT")
            quantity: Total quantity to sell
            duration: Execution duration in seconds
            position_side: Position side (LONG or SHORT)
            price_limit: Optional price limit (won't execute below this price)

        Returns:
            TWAP order details including order ID

        Example:
            # Execute 5 BTC over 30 minutes
            twap = client.twap().sell(
                symbol="BTC-USDT",
                quantity=5.0,
                duration=1800,
                position_side="SHORT"
            )
        """
        params = {
            "symbol": symbol,
            "side": "SELL",
            "positionSide": position_side,
            "quantity": quantity,
            "duration": duration,
        }
        if price_limit:
            params["priceLimit"] = price_limit

        return self.client.request("POST", "/openApi/swap/v2/trade/twapOrder", params)

    def get_order_detail(self, order_id: str) -> Dict[str, Any]:
        """
        Get TWAP order details

        Args:
            order_id: TWAP order ID

        Returns:
            Order details including execution progress, status, average price

        Example:
            details = client.twap().get_order_detail(twap['orderId'])
            progress = (float(details['executedQty']) / float(details['totalQty'])) * 100
            print(f"Progress: {progress:.2f}%")
        """
        return self.client.request(
            "GET",
            "/openApi/swap/v2/trade/twapOrder",
            {"orderId": order_id},
        )

    def get_open_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all open TWAP orders

        Args:
            symbol: Trading symbol (optional, returns all if not specified)

        Returns:
            List of open TWAP orders
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/swap/v2/trade/twapOpenOrders", params)

    def get_order_history(
        self,
        symbol: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Get TWAP order history

        Args:
            symbol: Trading symbol (optional)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            limit: Number of records to return

        Returns:
            Historical TWAP orders
        """
        params = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/swap/v2/trade/twapOrderHistory", params)

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel a TWAP order

        Args:
            order_id: TWAP order ID to cancel

        Returns:
            Cancellation confirmation

        Note:
            Only unfilled portion will be cancelled. Already executed parts remain.
        """
        return self.client.request(
            "DELETE",
            "/openApi/swap/v2/trade/twapOrder",
            {"orderId": order_id},
        )

    def cancel_all_orders(self, symbol: str) -> Dict[str, Any]:
        """
        Cancel all TWAP orders for a symbol

        Args:
            symbol: Trading symbol

        Returns:
            Cancellation confirmation for all orders
        """
        return self.client.request(
            "DELETE",
            "/openApi/swap/v2/trade/twapAllOrders",
            {"symbol": symbol},
        )
