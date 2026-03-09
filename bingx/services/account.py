"""
Account Service

Handles account operations including balance, positions, leverage, margin, etc.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class AccountService:
    """Service for account operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Account Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        return self.client.request("GET", "/openApi/swap/v2/user/balance")

    def get_positions(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get positions

        Args:
            symbol: Trading symbol (optional, returns all if not specified)
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self.client.request("GET", "/openApi/swap/v2/user/positions", params)

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        return self.client.request("GET", "/openApi/swap/v2/user/account")

    def get_leverage(self, symbol: str) -> Dict[str, Any]:
        """
        Get current leverage for a symbol

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/trade/leverage", {"symbol": symbol})

    def set_leverage(self, symbol: str, side: str, leverage: int) -> Dict[str, Any]:
        """
        Set leverage for a symbol

        Args:
            symbol: Trading symbol
            side: Position side (LONG, SHORT, BOTH)
            leverage: Leverage value
        """
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/leverage",
            {"symbol": symbol, "side": side, "leverage": leverage},
        )

    def get_margin_mode(self, symbol: str) -> Dict[str, Any]:
        """
        Get margin mode

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/trade/marginType", {"symbol": symbol})

    def set_margin_mode(self, symbol: str, margin_type: str) -> Dict[str, Any]:
        """
        Set margin mode

        Args:
            symbol: Trading symbol
            margin_type: Margin type (ISOLATED or CROSSED)
        """
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/marginType",
            {"symbol": symbol, "marginType": margin_type},
        )

    def set_position_margin(
        self, symbol: str, position_side: str, amount: float, type_: int
    ) -> Dict[str, Any]:
        """
        Adjust position margin

        Args:
            symbol: Trading symbol
            position_side: Position side (LONG, SHORT)
            amount: Margin amount
            type_: Type (1: add, 2: reduce)
        """
        return self.client.request(
            "POST",
            "/openApi/swap/v2/trade/positionMargin",
            {"symbol": symbol, "positionSide": position_side, "amount": amount, "type": type_},
        )

    def get_trading_fees(self, symbol: str) -> Dict[str, Any]:
        """
        Get trading fees for a symbol

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/user/commissionRate", {"symbol": symbol})

    def get_account_permissions(self) -> Dict[str, Any]:
        """Get API permissions"""
        return self.client.request("GET", "/openApi/swap/v2/user/apiPermissions")

    def get_api_key(self) -> Dict[str, Any]:
        """Get API key information"""
        return self.client.request("GET", "/openApi/swap/v2/user/apiKey")

    def get_user_commission_rates(self, symbol: str) -> Dict[str, Any]:
        """
        Get user commission rates

        Args:
            symbol: Trading symbol
        """
        return self.client.request("GET", "/openApi/swap/v2/user/commissionRate", {"symbol": symbol})

    def get_api_rate_limits(self) -> Dict[str, Any]:
        """Get API rate limits"""
        return self.client.request("GET", "/openApi/swap/v2/user/rateLimits")

    def get_balance_history(self, asset: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get balance history

        Args:
            asset: Asset name (e.g., 'USDT')
            limit: Number of records
        """
        return self.client.request(
            "GET",
            "/openApi/swap/v2/user/balanceHistory",
            {"asset": asset, "limit": limit},
        )

    def get_deposit_history(
        self, coin: Optional[str] = None, limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get deposit history

        Args:
            coin: Coin name (optional)
            limit: Number of records
        """
        params = {"limit": limit}
        if coin:
            params["coin"] = coin
        return self.client.request("GET", "/openApi/swap/v2/user/depositHistory", params)

    def get_withdraw_history(
        self, coin: Optional[str] = None, limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get withdrawal history

        Args:
            coin: Coin name (optional)
            limit: Number of records
        """
        params = {"limit": limit}
        if coin:
            params["coin"] = coin
        return self.client.request("GET", "/openApi/swap/v2/user/withdrawHistory", params)

    def get_asset_details(self, asset: str) -> Dict[str, Any]:
        """
        Get asset details

        Args:
            asset: Asset name
        """
        return self.client.request("GET", "/openApi/swap/v2/user/assetDetails", {"asset": asset})

    def get_all_assets(self) -> Dict[str, Any]:
        """Get all available assets"""
        return self.client.request("GET", "/openApi/swap/v2/user/assets")

    def get_funding_wallet(self, asset: Optional[str] = None) -> Dict[str, Any]:
        """
        Get funding wallet

        Args:
            asset: Asset name (optional)
        """
        params = {}
        if asset:
            params["asset"] = asset
        return self.client.request("GET", "/openApi/swap/v2/user/fundingWallet", params)

    def dust_transfer(self, assets: list) -> Dict[str, Any]:
        """
        Convert small assets to BNB

        Args:
            assets: List of asset names to convert
        """
        return self.client.request("POST", "/openApi/swap/v2/user/dustTransfer", {"assets": assets})
