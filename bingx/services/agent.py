"""
Agent Service

Handles BingX Agent (affiliate/broker) operations including invited users,
commission data, and partner information.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class AgentService:
    """Service for agent/affiliate operations"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Agent Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_invited_users(
        self,
        page_index: int = 1,
        page_size: int = 100,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        last_uid: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query invited users (paginated)

        Args:
            page_index: Page number (must be > 0)
            page_size: Page size (max 100)
            start_time: Start timestamp in milliseconds (max 30-day window)
            end_time: End timestamp in milliseconds
            last_uid: For pagination > 10,000 records, pass last UID from previous page
            recv_window: Request validity window in milliseconds
        """
        params: Dict[str, Any] = {"pageIndex": page_index, "pageSize": page_size}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if last_uid is not None:
            params["lastUid"] = last_uid
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self.client.request("GET", "/openApi/agent/v1/account/inviteAccountList", params)

    def get_daily_commission(
        self,
        start_time: str,
        end_time: str,
        page_index: int = 1,
        page_size: int = 100,
        uid: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query daily commission details (invitation relationship)

        Args:
            start_time: Start date string (e.g., "20240101"), max 30-day window
            end_time: End date string (e.g., "20240131")
            page_index: Page number (must be > 0)
            page_size: Page size (max 100)
            uid: Optional filter by specific invited user UID
            recv_window: Request validity window in milliseconds
        """
        params: Dict[str, Any] = {
            "startTime": start_time,
            "endTime": end_time,
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if uid is not None:
            params["uid"] = uid
        if recv_window is not None:
            params["recvWindow"] = recv_window
        return self.client.request("GET", "/openApi/agent/v2/reward/commissionDataList", params)

    def get_user_info(self, uid: int) -> Dict[str, Any]:
        """
        Query agent user information for a specific UID

        Args:
            uid: User UID to query
        """
        return self.client.request(
            "GET", "/openApi/agent/v1/account/inviteRelationCheck", {"uid": uid}
        )

    def get_api_commission(
        self,
        commission_biz_type: int,
        start_time: str,
        end_time: str,
        page_index: int = 1,
        page_size: int = 100,
        uid: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query API transaction commission (non-invitation relationship)

        Args:
            commission_biz_type: 81 = Perpetual contract, 82 = Spot trading
            start_time: Start date string (e.g., "20240101"), supports data after Dec 1, 2023
            end_time: End date string (e.g., "20240131")
            page_index: Page number (must be > 0)
            page_size: Page size (max 100)
            uid: Optional UID of the trading user
        """
        params: Dict[str, Any] = {
            "commissionBizType": commission_biz_type,
            "startTime": start_time,
            "endTime": end_time,
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if uid is not None:
            params["uid"] = uid
        return self.client.request(
            "GET", "/openApi/agent/v1/reward/third/commissionDataList", params
        )

    def get_partner_info(
        self,
        start_time: int,
        end_time: int,
        page_index: int = 1,
        page_size: int = 200,
        uid: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query partner information

        Args:
            start_time: Start date as integer (e.g., 20240101), supports last 3 months only
            end_time: End date as integer (e.g., 20240131)
            page_index: Page number (must be > 0)
            page_size: Page size (max 200)
            uid: Optional filter by specific partner UID
        """
        params: Dict[str, Any] = {
            "startTime": start_time,
            "endTime": end_time,
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if uid is not None:
            params["uid"] = uid
        return self.client.request("GET", "/openApi/agent/v1/asset/partnerData", params)

    def get_deposit_details(
        self,
        page_index: int = 1,
        page_size: int = 100,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        uid: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query deposit details of invited users

        Args:
            page_index: Page number (must be > 0)
            page_size: Page size (max 100)
            start_time: Start timestamp in milliseconds
            end_time: End timestamp in milliseconds
            uid: Optional filter by specific user UID
        """
        params: Dict[str, Any] = {"pageIndex": page_index, "pageSize": page_size}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if uid is not None:
            params["uid"] = uid
        return self.client.request("GET", "/openApi/agent/v1/asset/depositDetailList", params)

    def get_referral_code_commission(
        self,
        start_time: str,
        end_time: str,
        page_index: int = 1,
        page_size: int = 100,
        referral_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query invitation code commission data

        Args:
            start_time: Start date string (e.g., "20240101")
            end_time: End date string (e.g., "20240131")
            page_index: Page number (must be > 0)
            page_size: Page size (max 100)
            referral_code: Optional specific referral code to query
        """
        params: Dict[str, Any] = {
            "startTime": start_time,
            "endTime": end_time,
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if referral_code:
            params["referralCode"] = referral_code
        return self.client.request(
            "GET", "/openApi/agent/v1/commissionDataList/referralCode", params
        )

    def check_superior_agent(self, uid: int) -> Dict[str, Any]:
        """
        Check if a user is a superior agent

        Args:
            uid: User UID to check
        """
        return self.client.request(
            "GET", "/openApi/agent/v1/account/superiorCheck", {"uid": uid}
        )
