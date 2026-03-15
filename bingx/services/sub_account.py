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
        wallet_type: int,
        amount: float,
        user_account_type: int,
        user_account: str,
        calling_code: Optional[str] = None,
        transfer_client_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Sub-account internal transfer

        Args:
            coin: Coin name
            wallet_type: Wallet type (1=Fund Account, 2=Standard Futures, 3=Perpetual Futures, 15=Spot Account)
            amount: Transfer amount
            user_account_type: User account type (1=UID, 2=Phone number, 3=Email)
            user_account: User account (UID, phone number, or email)
            calling_code: Phone area code (required when user_account_type=2)
            transfer_client_id: Client-defined internal transfer ID (alphanumeric, max 100 chars)
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
        return self.client.request("POST", "/openApi/wallets/v1/capital/subAccountInnerTransfer/apply", params)

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

    def sub_mother_account_asset_transfer(
        self,
        asset_name: str,
        transfer_amount: float,
        from_uid: int,
        from_type: int,
        from_account_type: int,
        to_uid: int,
        to_type: int,
        to_account_type: int,
        remark: str,
        recv_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Sub-Mother Account Asset Transfer Interface
        
        Note: This endpoint is only available to the master account.

        Args:
            asset_name: Asset name (e.g., USDT)
            transfer_amount: Transfer amount
            from_uid: Payer UID
            from_type: Payer sub-account type (1=Parent account, 2=Sub-account)
            from_account_type: Payer account type (1=Funding, 2=Standard futures, 3=Perpetual U-based, 15=Spot)
            to_uid: Receiver UID
            to_type: Receiver sub-account type (1=Parent account, 2=Sub-account)
            to_account_type: Receiver account type (1=Funding, 2=Standard futures, 3=Perpetual U-based, 15=Spot)
            remark: Transfer remarks
            recv_window: Execution window time (cannot exceed 60000)
            
        Returns:
            Response with tranId (transfer record ID)
        """
        params = {
            "assetName": asset_name,
            "transferAmount": transfer_amount,
            "fromUid": from_uid,
            "fromType": from_type,
            "fromAccountType": from_account_type,
            "toUid": to_uid,
            "toType": to_type,
            "toAccountType": to_account_type,
            "remark": remark,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self.client.request("POST", "/openApi/account/transfer/v1/subAccount/transferAsset", params)

    def get_sub_mother_account_transferable_amount(
        self,
        from_uid: int,
        from_account_type: int,
        to_uid: int,
        to_account_type: int,
        recv_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query Sub-Mother Account Transferable Amount
        
        Note: This endpoint is only available to the master account.

        Args:
            from_uid: Payer UID
            from_account_type: Payer account type (1=Funding, 2=Standard futures, 3=Perpetual U-Based)
            to_uid: Receiver UID
            to_account_type: Receiver account type (1=Funding, 2=Standard futures, 3=Perpetual U-Based)
            recv_window: Execution window time (cannot exceed 60000)
            
        Returns:
            Response with coins array containing id, name, and availableAmount
        """
        params = {
            "fromUid": from_uid,
            "fromAccountType": from_account_type,
            "toUid": to_uid,
            "toAccountType": to_account_type,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self.client.request("POST", "/openApi/account/transfer/v1/subAccount/transferAsset/supportCoins", params)

    def get_sub_mother_account_transfer_history(
        self,
        uid: int,
        type_: Optional[str] = None,
        tran_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page_id: Optional[int] = None,
        paging_size: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query Sub-Mother Account Transfer History
        
        Note: This endpoint is only available to the master account.

        Args:
            uid: UID to query
            type_: Transfer type filter (optional)
            tran_id: Transfer ID (optional)
            start_time: Start time in milliseconds (optional)
            end_time: End time in milliseconds (optional)
            page_id: Current page (default 1)
            paging_size: Page size (default 10, max 100)
            recv_window: Execution window time (cannot exceed 60000)
            
        Returns:
            Response with total count and rows array
        """
        params = {"uid": uid}
        if type_:
            params["type"] = type_
        if tran_id:
            params["tranId"] = tran_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if page_id is not None:
            params["pageId"] = page_id
        if paging_size is not None:
            params["pagingSize"] = paging_size
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self.client.request("GET", "/openApi/account/transfer/v1/subAccount/asset/transferHistory", params)
