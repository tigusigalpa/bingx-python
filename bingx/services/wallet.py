"""
Wallet Service

Handles wallet operations including deposits, withdrawals, and wallet addresses.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class WalletService:
    """Service for wallet operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Wallet Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_deposit_history(
        self,
        coin: Optional[str] = None,
        status: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get deposit history

        Args:
            coin: Coin name (optional)
            status: Deposit status (0: pending, 1: success, 6: credited but cannot withdraw)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            limit: Number of records
        """
        params = {"limit": limit}
        if coin:
            params["coin"] = coin
        if status is not None:
            params["status"] = status
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/api/v3/capital/deposit/hisrec", params)

    def get_deposit_address(self, coin: str, network: str) -> Dict[str, Any]:
        """
        Get deposit address

        Args:
            coin: Coin name (e.g., 'USDT')
            network: Network name (e.g., 'TRC20')
        """
        return self.client.request(
            "GET",
            "/openApi/api/v3/capital/deposit/address",
            {"coin": coin, "network": network},
        )

    def get_withdrawal_history(
        self,
        coin: Optional[str] = None,
        status: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get withdrawal history

        Args:
            coin: Coin name (optional)
            status: Withdrawal status (0: pending, 1: processing, 2: success, 3: failed, 4: rejected, 5: cancelled, 6: credited but cannot withdraw)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            limit: Number of records
        """
        params = {"limit": limit}
        if coin:
            params["coin"] = coin
        if status is not None:
            params["status"] = status
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/api/v3/capital/withdraw/history", params)

    def withdraw(
        self,
        coin: str,
        address: str,
        amount: float,
        network: str,
        address_tag: Optional[str] = None,
        withdraw_order_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a withdrawal

        Args:
            coin: Coin name
            address: Withdrawal address
            amount: Withdrawal amount
            network: Network name
            address_tag: Address tag (optional, for some coins)
            withdraw_order_id: Custom withdrawal order ID (optional)
        """
        params = {"coin": coin, "address": address, "amount": amount, "network": network}
        if address_tag:
            params["addressTag"] = address_tag
        if withdraw_order_id:
            params["withdrawOrderId"] = withdraw_order_id
        return self.client.request("POST", "/openApi/api/v3/capital/withdraw/apply", params)

    def get_all_coin_info(self) -> Dict[str, Any]:
        """Get information for all coins"""
        return self.client.request("GET", "/openApi/api/v3/capital/config/getall")
