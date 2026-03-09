"""
Trade Service

Handles trading operations including orders, positions, and commission calculations.
"""

from typing import Any, Dict, List, Optional

from ..http.base_client import BaseHTTPClient


class TradeService:
    """Service for trading operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Trade Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def create_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order

        Args:
            params: Order parameters (symbol, side, type, quantity, etc.)
        """
        return self.client.request("POST", "/openApi/swap/v2/trade/order", params)

    def create_test_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test order creation (no execution)

        Args:
            params: Order parameters
        """
        return self.client.request("POST", "/openApi/swap/v2/trade/order/test", params)

    def create_batch_orders(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple orders at once

        Args:
            orders: List of order parameters
        """
        return self.client.request("POST", "/openApi/swap/v2/trade/batchOrders", {"batchOrders": orders})

    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order

        Args:
            symbol: Trading symbol
            order_id: Order ID
        """
        return self.client.request("DELETE", "/openApi/swap/v2/trade/order", {"symbol": symbol, "orderId": order_id})

    def cancel_all_orders(self, symbol: str) -> Dict[str, Any]:
        """
        Cancel all orders for a symbol

        Args:
            symbol: Trading symbol
        """
        return self.client.request("DELETE", "/openApi/swap/v2/trade/allOpenOrders", {"symbol": symbol})

    def cancel_batch_orders(self, symbol: str, order_ids: List[str]) -> Dict[str, Any]:
        """
        Cancel multiple orders

        Args:
            symbol: Trading symbol
            order_ids: List of order IDs
        """
        return self.client.request(
            "DELETE",
            "/openApi/swap/v2/trade/batchOrders",
            {"symbol": symbol, "orderIdList": order_ids},
        )

    def cancel_and_replace_order(
        self,
        symbol: str,
        cancel_order_id: str,
        side: str,
        type_: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Cancel an order and create a new one

        Args:
            symbol: Trading symbol
            cancel_order_id: Order ID to cancel
            side: Order side (BUY, SELL)
            type_: Order type (LIMIT, MARKET)
            quantity: Order quantity
            price: Order price (for LIMIT orders)
        """
        params = {
            "symbol": symbol,
            "cancelOrderId": cancel_order_id,
            "side": side,
            "type": type_,
            "quantity": quantity,
        }
        if price:
            params["price"] = price
        return self.client.request("POST", "/openApi/swap/v2/trade/cancelReplace", params)

    def get_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Get order details

        Args:
            symbol: Trading symbol
            order_id: Order ID
        """
        return self.client.request("GET", "/openApi/swap/v2/trade/order", {"symbol": symbol, "orderId": order_id})

    def get_open_orders(self, symbol: Optional[str] = None, limit: int = 500) -> Dict[str, Any]:
        """
        Get open orders

        Args:
            symbol: Trading symbol (optional)
            limit: Number of orders
        """
        params = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/swap/v2/trade/openOrders", params)

    def get_order_history(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get order history

        Args:
            symbol: Trading symbol
            limit: Number of orders
        """
        return self.client.request("GET", "/openApi/swap/v2/trade/allOrders", {"symbol": symbol, "limit": limit})

    def get_user_trades(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get user trade history

        Args:
            symbol: Trading symbol
            limit: Number of trades
        """
        return self.client.request("GET", "/openApi/swap/v2/trade/userTrades", {"symbol": symbol, "limit": limit})

    def spot_market_buy(self, symbol: str, quantity: float) -> Dict[str, Any]:
        """
        Create spot market buy order

        Args:
            symbol: Trading symbol
            quantity: Order quantity
        """
        return self.client.request(
            "POST",
            "/openApi/spot/v1/trade/order",
            {"symbol": symbol, "side": "BUY", "type": "MARKET", "quantity": quantity},
        )

    def spot_market_sell(self, symbol: str, quantity: float) -> Dict[str, Any]:
        """
        Create spot market sell order

        Args:
            symbol: Trading symbol
            quantity: Order quantity
        """
        return self.client.request(
            "POST",
            "/openApi/spot/v1/trade/order",
            {"symbol": symbol, "side": "SELL", "type": "MARKET", "quantity": quantity},
        )

    def spot_limit_buy(self, symbol: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Create spot limit buy order

        Args:
            symbol: Trading symbol
            quantity: Order quantity
            price: Order price
        """
        return self.client.request(
            "POST",
            "/openApi/spot/v1/trade/order",
            {"symbol": symbol, "side": "BUY", "type": "LIMIT", "quantity": quantity, "price": price},
        )

    def spot_limit_sell(self, symbol: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Create spot limit sell order

        Args:
            symbol: Trading symbol
            quantity: Order quantity
            price: Order price
        """
        return self.client.request(
            "POST",
            "/openApi/spot/v1/trade/order",
            {"symbol": symbol, "side": "SELL", "type": "LIMIT", "quantity": quantity, "price": price},
        )

    def futures_long_market(self, symbol: str, margin: float, leverage: int) -> Dict[str, Any]:
        """
        Create futures long market order

        Args:
            symbol: Trading symbol
            margin: Margin amount
            leverage: Leverage
        """
        quantity = margin * leverage
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/order",
            {
                "symbol": symbol,
                "side": "BUY",
                "positionSide": "LONG",
                "type": "MARKET",
                "quantity": quantity,
            },
        )

    def futures_short_market(self, symbol: str, margin: float, leverage: int) -> Dict[str, Any]:
        """
        Create futures short market order

        Args:
            symbol: Trading symbol
            margin: Margin amount
            leverage: Leverage
        """
        quantity = margin * leverage
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/order",
            {
                "symbol": symbol,
                "side": "SELL",
                "positionSide": "SHORT",
                "type": "MARKET",
                "quantity": quantity,
            },
        )

    def futures_long_limit(
        self,
        symbol: str,
        margin: float,
        price: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        leverage: int = 1,
    ) -> Dict[str, Any]:
        """
        Create futures long limit order with optional SL/TP

        Args:
            symbol: Trading symbol
            margin: Margin amount
            price: Order price
            stop_loss: Stop loss price (optional)
            take_profit: Take profit price (optional)
            leverage: Leverage
        """
        quantity = margin * leverage
        params = {
            "symbol": symbol,
            "side": "BUY",
            "positionSide": "LONG",
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
        }
        if stop_loss:
            params["stopLoss"] = stop_loss
        if take_profit:
            params["takeProfit"] = take_profit
        return self.client.request("POST", "/openApi/swap/v2/trade/order", params)

    def calculate_futures_commission(self, margin: float, leverage: int) -> Dict[str, Any]:
        """
        Calculate futures commission

        Args:
            margin: Margin amount
            leverage: Leverage

        Returns:
            Dictionary with commission details
        """
        position_value = margin * leverage
        maker_fee_rate = 0.0002
        taker_fee_rate = 0.0005

        return {
            "position_value": position_value,
            "maker_fee": position_value * maker_fee_rate,
            "taker_fee": position_value * taker_fee_rate,
            "maker_fee_rate": maker_fee_rate,
            "taker_fee_rate": taker_fee_rate,
        }

    def get_commission_amount(self, margin: float, leverage: int) -> float:
        """
        Get commission amount (taker fee)

        Args:
            margin: Margin amount
            leverage: Leverage

        Returns:
            Commission amount
        """
        commission = self.calculate_futures_commission(margin, leverage)
        return commission["taker_fee"]

    def calculate_batch_commission(self, orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate commission for multiple orders

        Args:
            orders: List of order dictionaries with 'margin' and 'leverage' keys

        Returns:
            List of commission details
        """
        return [
            self.calculate_futures_commission(order["margin"], order["leverage"])
            for order in orders
        ]

    def get_commission_rates(self) -> Dict[str, float]:
        """Get commission rates"""
        return {"maker": 0.0002, "taker": 0.0005}

    def get_position_mode(self) -> Dict[str, Any]:
        """Get position mode"""
        return self.client.request("GET", "/openApi/swap/v2/trade/positionSide/dual")

    def set_position_mode(self, dual_side_position: str) -> Dict[str, Any]:
        """
        Set position mode

        Args:
            dual_side_position: Position mode (HEDGE_MODE or ONE_WAY_MODE)
        """
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/positionSide/dual",
            {"dualSidePosition": dual_side_position},
        )

    def get_position_side(self) -> Dict[str, Any]:
        """Get position side"""
        return self.client.request("GET", "/openApi/swap/v2/trade/positionSide")

    def set_position_side(self, position_side: str) -> Dict[str, Any]:
        """
        Set position side

        Args:
            position_side: Position side (BOTH, LONG, SHORT)
        """
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/positionSide",
            {"positionSide": position_side},
        )

    def close_all_positions(self, symbol: str) -> Dict[str, Any]:
        """
        Close all positions for a symbol

        Args:
            symbol: Trading symbol
        """
        return self.client.request("POST", "/openApi/swap/v2/trade/closeAllPositions", {"symbol": symbol})

    def get_margin_type(self, symbol: str) -> Dict[str, Any]:
        """
        Get margin type

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/trade/marginType", {"symbol": symbol})

    def change_margin_type(self, symbol: str, margin_type: str) -> Dict[str, Any]:
        """
        Change margin type

        Args:
            symbol: Trading symbol
            margin_type: Margin type (ISOLATED or CROSSED)
        """
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/marginType",
            {"symbol": symbol, "marginType": margin_type},
        )
