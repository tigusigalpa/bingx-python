"""
Coin-M Trade Service

Handles Coin-M perpetual futures trading operations.
"""

from typing import Any, Dict, List, Optional

from ...http.base_client import BaseHTTPClient


class CoinMTradeService:
    """Service for Coin-M trading operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Coin-M Trade Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def create_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a Coin-M order

        Args:
            params: Order parameters (symbol, side, type, quantity, etc.)
        """
        return self.client.request("POST", "/openApi/cswap/v1/trade/order", params)

    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Cancel a Coin-M order

        Args:
            symbol: Trading symbol
            order_id: Order ID
        """
        return self.client.request(
            "DELETE", "/openApi/cswap/v1/trade/order", {"symbol": symbol, "orderId": order_id}
        )

    def cancel_all_orders(self, symbol: str) -> Dict[str, Any]:
        """
        Cancel all Coin-M orders for a symbol

        Args:
            symbol: Trading symbol
        """
        return self.client.request(
            "DELETE", "/openApi/cswap/v1/trade/allOpenOrders", {"symbol": symbol}
        )

    def get_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Get Coin-M order details

        Args:
            symbol: Trading symbol
            order_id: Order ID
        """
        return self.client.request(
            "GET", "/openApi/cswap/v1/trade/order", {"symbol": symbol, "orderId": order_id}
        )

    def get_open_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get open Coin-M orders

        Args:
            symbol: Trading symbol (optional)
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/cswap/v1/trade/openOrders", params)

    def get_positions(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Coin-M positions

        Args:
            symbol: Trading symbol (optional)
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/cswap/v1/user/positions", params)

    def get_balance(self) -> Dict[str, Any]:
        """Get Coin-M account balance"""
        return self.client.request("GET", "/openApi/cswap/v1/user/balance")

    def set_leverage(self, symbol: str, side: str, leverage: int) -> Dict[str, Any]:
        """
        Set leverage for Coin-M contract

        Args:
            symbol: Trading symbol
            side: Position side (LONG, SHORT, BOTH)
            leverage: Leverage value
        """
        return self.client.request(
            "POST",
            "/openApi/cswap/v1/trade/leverage",
            {"symbol": symbol, "side": side, "leverage": leverage},
        )

    def set_margin_mode(self, symbol: str, margin_type: str) -> Dict[str, Any]:
        """
        Set margin mode for Coin-M contract

        Args:
            symbol: Trading symbol
            margin_type: Margin type (ISOLATED or CROSSED)
        """
        return self.client.request(
            "POST",
            "/openApi/cswap/v1/trade/marginType",
            {"symbol": symbol, "marginType": margin_type},
        )

    def adjust_position_margin(
        self, symbol: str, amount: float, type_: int
    ) -> Dict[str, Any]:
        """
        Adjust position margin for Coin-M contract

        Args:
            symbol: Trading symbol
            amount: Margin amount
            type_: Type (1: add, 2: reduce)
        """
        return self.client.request(
            "POST",
            "/openApi/cswap/v1/trade/positionMargin",
            {"symbol": symbol, "amount": amount, "type": type_},
        )

    def get_order_history(
        self, symbol: str, limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get Coin-M order history

        Args:
            symbol: Trading symbol
            limit: Number of orders
        """
        return self.client.request(
            "GET", "/openApi/cswap/v1/trade/allOrders", {"symbol": symbol, "limit": limit}
        )

    def get_user_trades(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get Coin-M user trade history

        Args:
            symbol: Trading symbol
            limit: Number of trades
        """
        return self.client.request(
            "GET", "/openApi/cswap/v1/trade/userTrades", {"symbol": symbol, "limit": limit}
        )

    def get_income_history(
        self,
        symbol: Optional[str] = None,
        income_type: Optional[str] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get Coin-M income history

        Args:
            symbol: Trading symbol (optional)
            income_type: Income type (optional)
            limit: Number of records
        """
        params = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        if income_type:
            params["incomeType"] = income_type
        return self.client.request("GET", "/openApi/cswap/v1/user/income", params)

    def get_commission_rate(self, symbol: str) -> Dict[str, Any]:
        """
        Get commission rate for Coin-M contract

        Args:
            symbol: Trading symbol
        """
        return self.client.request(
            "GET", "/openApi/cswap/v1/user/commissionRate", {"symbol": symbol}
        )
