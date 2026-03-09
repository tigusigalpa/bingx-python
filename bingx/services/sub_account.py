"""
Sub-Account Service

Handles sub-account management operations.
"""

from typing import Any, Dict, List, Optional

from ..http.base_client import BaseHTTPClient


class SubAccountService:
    """Service for sub-account management"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Sub-Account Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def create_sub_account(self, sub_account_string: str) -> Dict[str, Any]:
        """
        Create a new sub-account

        Args:
            sub_account_string: Sub-account identifier
        """
        return self.client.request(
            "POST",
            "/openApi/api/v3/sub-account/create",
            {"subAccountString": sub_account_string},
        )

    def get_account_uid(self) -> Dict[str, Any]:
        """Get account UID"""
        return self.client.request("GET", "/openApi/api/v3/account/uid")

    def get_sub_account_list(
        self,
        sub_account_string: Optional[str] = None,
        current: int = 1,
        size: int = 10,
    ) -> Dict[str, Any]:
        """
        Get list of sub-accounts

        Args:
            sub_account_string: Sub-account identifier (optional)
            current: Current page
            size: Page size
        """
        params = {"current": current, "size": size}
        if sub_account_string:
            params["subAccountString"] = sub_account_string
        return self.client.request("GET", "/openApi/api/v3/sub-account/list", params)

    def get_sub_account_assets(self, sub_uid: str) -> Dict[str, Any]:
        """
        Get sub-account assets

        Args:
            sub_uid: Sub-account UID
        """
        return self.client.request("GET", "/openApi/api/v3/sub-account/assets", {"subUid": sub_uid})

    def update_sub_account_status(self, sub_account_string: str, status: int) -> Dict[str, Any]:
        """
        Update sub-account status

        Args:
            sub_account_string: Sub-account identifier
            status: Status (1: enable, 2: disable)
        """
        return self.client.request(
            "POST",
            "/openApi/api/v3/sub-account/status",
            {"subAccountString": sub_account_string, "status": status},
        )

    def get_all_sub_account_balances(self) -> Dict[str, Any]:
        """Get all sub-account balances"""
        return self.client.request("GET", "/openApi/api/v3/sub-account/balances")

    def create_sub_account_api_key(
        self,
        sub_account_string: str,
        label: str,
        permissions: Dict[str, bool],
        ip: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create API key for sub-account

        Args:
            sub_account_string: Sub-account identifier
            label: API key label
            permissions: Permissions dictionary (e.g., {'spot': True, 'futures': True})
            ip: IP whitelist (optional)
        """
        params = {
            "subAccountString": sub_account_string,
            "label": label,
            "permissions": permissions,
        }
        if ip:
            params["ip"] = ip
        return self.client.request("POST", "/openApi/api/v3/sub-account/apiKey", params)

    def query_api_key(self, sub_account_string: str) -> Dict[str, Any]:
        """
        Query API key information

        Args:
            sub_account_string: Sub-account identifier
        """
        return self.client.request(
            "GET",
            "/openApi/api/v3/sub-account/apiKey",
            {"subAccountString": sub_account_string},
        )

    def edit_sub_account_api_key(
        self,
        sub_account_string: str,
        api_key: str,
        permissions: Dict[str, bool],
        ip: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Edit sub-account API key

        Args:
            sub_account_string: Sub-account identifier
            api_key: API key to edit
            permissions: New permissions
            ip: New IP whitelist (optional)
        """
        params = {
            "subAccountString": sub_account_string,
            "apiKey": api_key,
            "permissions": permissions,
        }
        if ip:
            params["ip"] = ip
        return self.client.request("PUT", "/openApi/api/v3/sub-account/apiKey", params)

    def delete_sub_account_api_key(self, sub_account_string: str, api_key: str) -> Dict[str, Any]:
        """
        Delete sub-account API key

        Args:
            sub_account_string: Sub-account identifier
            api_key: API key to delete
        """
        return self.client.request(
            "DELETE",
            "/openApi/api/v3/sub-account/apiKey",
            {"subAccountString": sub_account_string, "apiKey": api_key},
        )

    def authorize_sub_account_internal_transfer(
        self, sub_account_string: str, authorize: int
    ) -> Dict[str, Any]:
        """
        Authorize sub-account for internal transfers

        Args:
            sub_account_string: Sub-account identifier
            authorize: Authorization (1: authorize, 0: revoke)
        """
        return self.client.request(
            "POST",
            "/openApi/api/v3/sub-account/authorize",
            {"subAccountString": sub_account_string, "authorize": authorize},
        )

    def sub_account_internal_transfer(
        self,
        coin: str,
        wallet_type: str,
        amount: float,
        transfer_type: str,
        from_sub_uid: Optional[str] = None,
        to_sub_uid: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Internal transfer between main and sub-accounts

        Args:
            coin: Coin name
            wallet_type: Wallet type (SPOT, PERPETUAL)
            amount: Transfer amount
            transfer_type: Transfer type (FROM_MAIN_TO_SUB, FROM_SUB_TO_MAIN, FROM_SUB_TO_SUB)
            from_sub_uid: Source sub-account UID (for FROM_SUB_TO_MAIN or FROM_SUB_TO_SUB)
            to_sub_uid: Destination sub-account UID (for FROM_MAIN_TO_SUB or FROM_SUB_TO_SUB)
            client_id: Client ID (optional)
        """
        params = {
            "coin": coin,
            "walletType": wallet_type,
            "amount": amount,
            "transferType": transfer_type,
        }
        if from_sub_uid:
            params["fromSubUid"] = from_sub_uid
        if to_sub_uid:
            params["toSubUid"] = to_sub_uid
        if client_id:
            params["clientId"] = client_id
        return self.client.request("POST", "/openApi/api/v3/sub-account/internal/transfer", params)

    def get_sub_account_internal_transfer_records(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        current: int = 1,
        size: int = 50,
    ) -> Dict[str, Any]:
        """
        Get internal transfer records

        Args:
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            current: Current page
            size: Page size
        """
        params = {"current": current, "size": size}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/api/v3/sub-account/internal/transfer/records", params)

    def sub_account_asset_transfer(
        self, sub_uid: str, type_: str, asset: str, amount: float
    ) -> Dict[str, Any]:
        """
        Sub-account asset transfer

        Args:
            sub_uid: Sub-account UID
            type_: Transfer type (e.g., 'FUND_PFUTURES')
            asset: Asset name
            amount: Transfer amount
        """
        return self.client.request(
            "POST",
            "/openApi/api/v3/sub-account/asset/transfer",
            {"subUid": sub_uid, "type": type_, "asset": asset, "amount": amount},
        )

    def get_sub_account_transfer_supported_coins(self, sub_uid: str) -> Dict[str, Any]:
        """
        Get supported coins for sub-account transfers

        Args:
            sub_uid: Sub-account UID
        """
        return self.client.request(
            "GET",
            "/openApi/api/v3/sub-account/transfer/supportedCoins",
            {"subUid": sub_uid},
        )

    def get_sub_account_asset_transfer_history(
        self,
        sub_uid: str,
        type_: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        current: int = 1,
        size: int = 50,
    ) -> Dict[str, Any]:
        """
        Get asset transfer history

        Args:
            sub_uid: Sub-account UID
            type_: Transfer type
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            current: Current page
            size: Page size
        """
        params = {"subUid": sub_uid, "type": type_, "current": current, "size": size}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/api/v3/sub-account/asset/transfer/history", params)

    def create_sub_account_deposit_address(
        self, coin: str, network: str, sub_uid: str
    ) -> Dict[str, Any]:
        """
        Create deposit address for sub-account

        Args:
            coin: Coin name
            network: Network name
            sub_uid: Sub-account UID
        """
        return self.client.request(
            "POST",
            "/openApi/api/v3/sub-account/deposit/address",
            {"coin": coin, "network": network, "subUid": sub_uid},
        )

    def get_sub_account_deposit_address(
        self, coin: str, sub_uid: str, network: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get sub-account deposit address

        Args:
            coin: Coin name
            sub_uid: Sub-account UID
            network: Network name (optional)
        """
        params = {"coin": coin, "subUid": sub_uid}
        if network:
            params["network"] = network
        return self.client.request("GET", "/openApi/api/v3/sub-account/deposit/address", params)

    def get_sub_account_deposit_history(
        self,
        sub_uid: str,
        coin: Optional[str] = None,
        status: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get sub-account deposit history

        Args:
            sub_uid: Sub-account UID
            coin: Coin name (optional)
            status: Deposit status (optional)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            limit: Number of records
        """
        params = {"subUid": sub_uid, "limit": limit}
        if coin:
            params["coin"] = coin
        if status is not None:
            params["status"] = status
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self.client.request("GET", "/openApi/api/v3/sub-account/deposit/history", params)
