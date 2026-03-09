"""
Copy Trading Service

Handles copy trading operations for both perpetual futures and spot.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class CopyTradingService:
    """Service for copy trading operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Copy Trading Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_current_track_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current track orders (perpetual futures)

        Args:
            symbol: Trading symbol (optional)
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/copy/v1/trader/getCurrentTrackOrders", params)

    def close_track_order(self, position_id: str) -> Dict[str, Any]:
        """
        Close position by order number (perpetual futures)

        Args:
            position_id: Position ID
        """
        return self.client.request(
            "POST",
            "/openApi/copy/v1/trader/closeTrackOrder",
            {"positionId": position_id},
        )

    def set_tpsl(
        self,
        position_id: str,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Set take profit and stop loss (perpetual futures)

        Args:
            position_id: Position ID
            stop_loss: Stop loss price (optional)
            take_profit: Take profit price (optional)
        """
        params = {"positionId": position_id}
        if stop_loss:
            params["stopLoss"] = stop_loss
        if take_profit:
            params["takeProfit"] = take_profit
        return self.client.request("POST", "/openApi/copy/v1/trader/setTPSL", params)

    def get_trader_detail(self) -> Dict[str, Any]:
        """Get trader details (perpetual futures)"""
        return self.client.request("GET", "/openApi/copy/v1/trader/detail")

    def get_profit_summary(self) -> Dict[str, Any]:
        """Get profit summary (perpetual futures)"""
        return self.client.request("GET", "/openApi/copy/v1/trader/profitSummary")

    def get_profit_detail(self, page_index: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Get profit details with pagination (perpetual futures)

        Args:
            page_index: Page index
            page_size: Page size
        """
        return self.client.request(
            "GET",
            "/openApi/copy/v1/trader/profitDetail",
            {"pageIndex": page_index, "pageSize": page_size},
        )

    def set_commission(self, commission_rate: float) -> Dict[str, Any]:
        """
        Set commission rate (perpetual futures)

        Args:
            commission_rate: Commission rate (e.g., 5.0 for 5%)
        """
        return self.client.request(
            "POST",
            "/openApi/copy/v1/trader/setCommission",
            {"commissionRate": commission_rate},
        )

    def get_trading_pairs(self) -> Dict[str, Any]:
        """Get available trading pairs (perpetual futures)"""
        return self.client.request("GET", "/openApi/copy/v1/trader/tradingPairs")

    def sell_spot_order(self, buy_order_id: str) -> Dict[str, Any]:
        """
        Sell spot order based on buy order ID

        Args:
            buy_order_id: Buy order ID
        """
        return self.client.request(
            "POST",
            "/openApi/copy/v1/trader/spot/sellOrder",
            {"buyOrderId": buy_order_id},
        )

    def get_spot_trader_detail(self) -> Dict[str, Any]:
        """Get spot trader details"""
        return self.client.request("GET", "/openApi/copy/v1/trader/spot/detail")

    def get_spot_profit_summary(self) -> Dict[str, Any]:
        """Get spot profit summary"""
        return self.client.request("GET", "/openApi/copy/v1/trader/spot/profitSummary")

    def get_spot_profit_detail(self, page_index: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Get spot profit details

        Args:
            page_index: Page index
            page_size: Page size
        """
        return self.client.request(
            "GET",
            "/openApi/copy/v1/trader/spot/profitDetail",
            {"pageIndex": page_index, "pageSize": page_size},
        )

    def get_spot_history_orders(self, page_index: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """
        Query historical spot orders

        Args:
            page_index: Page index
            page_size: Page size
        """
        return self.client.request(
            "GET",
            "/openApi/copy/v1/trader/spot/historyOrders",
            {"pageIndex": page_index, "pageSize": page_size},
        )
