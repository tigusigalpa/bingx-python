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
        wallet_type: int,
        amount: float,
        user_account_type: int,
        user_account: str,
        calling_code: Optional[str] = None,
        transfer_client_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Internal transfer (main account internal transfer)

        Args:
            coin: Coin name
            wallet_type: Wallet type (1=Fund Account, 2=Standard Futures, 3=Perpetual Futures, 4=Spot Account)
            amount: Transfer amount
            user_account_type: User account type (1=UID, 2=Phone number, 3=Email)
            user_account: User account (UID, phone number, or email)
            calling_code: Area code for telephone (required when user_account_type=2)
            transfer_client_id: Custom ID for internal transfer (alphanumeric, max 100 chars)
            recv_window: Request validity time window in milliseconds
        """
        params = {
            "coin": coin,
            "walletType": wallet_type,
            "amount": amount,
            "userAccountType": user_account_type,
            "userAccount": user_account,
        }
        if calling_code:
            params["callingCode"] = calling_code
        if transfer_client_id:
            params["transferClientId"] = transfer_client_id
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self.client.request("POST", "/openApi/wallets/v1/capital/innerTransfer/apply", params)

    def get_all_account_balances(self) -> Dict[str, Any]:
        """Get all account balances"""
        return self.client.request("GET", "/openApi/api/v3/asset/accountBalances")
