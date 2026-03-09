"""
Spot Account Service

Handles spot account operations including balance, transfers, and internal transfers.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class SpotAccountService:
    """Service for spot account operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Spot Account Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_balance(self) -> Dict[str, Any]:
        """Get spot account balance"""
        return self.client.request("GET", "/openApi/spot/v1/account/balance")

    def get_fund_balance(self) -> Dict[str, Any]:
        """Get fund balance"""
        return self.client.request("GET", "/openApi/api/v3/asset/transfer")

    def universal_transfer(
        self, type_: str, asset: str, amount: float, from_symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Universal transfer between accounts

        Args:
            type_: Transfer type (e.g., 'FUND_PFUTURES', 'PFUTURES_FUND')
            asset: Asset name (e.g., 'USDT')
            amount: Transfer amount
            from_symbol: Source symbol (optional)
        """
        params = {"type": type_, "asset": asset, "amount": amount}
        if from_symbol:
            params["fromSymbol"] = from_symbol
        return self.client.request("POST", "/openApi/api/v3/asset/transfer", params)

    def get_asset_transfer_records(
        self,
        type_: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        current: int = 1,
        size: int = 10,
    ) -> Dict[str, Any]:
        """
        Get asset transfer records

        Args:
            type_: Transfer type
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            current: Current page
            size: Page size
        """
        params = {"type": type_, "current": current, "size": size}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/api/v3/asset/transfer", params)

    def internal_transfer(
        self,
        coin: str,
        wallet_type: str,
        amount: float,
        transfer_type: str,
        sub_uid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Internal transfer (main <-> sub account)

        Args:
            coin: Coin name
            wallet_type: Wallet type (SPOT, PERPETUAL)
            amount: Transfer amount
            transfer_type: Transfer type (FROM_MAIN_TO_SUB, FROM_SUB_TO_MAIN)
            sub_uid: Sub-account UID
        """
        params = {
            "coin": coin,
            "walletType": wallet_type,
            "amount": amount,
            "transferType": transfer_type,
        }
        if sub_uid:
            params["subUid"] = sub_uid
        return self.client.request("POST", "/openApi/api/v3/asset/internal/transfer", params)

    def get_all_account_balances(self) -> Dict[str, Any]:
        """Get all account balances"""
        return self.client.request("GET", "/openApi/api/v3/asset/accountBalances")
