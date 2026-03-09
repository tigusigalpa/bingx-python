"""
Listen Key Service

Handles WebSocket authentication listen keys.
"""

from typing import Any, Dict

from ..http.base_client import BaseHTTPClient


class ListenKeyService:
    """Service for WebSocket listen key management"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Listen Key Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def generate(self) -> Dict[str, Any]:
        """
        Generate a new listen key

        Returns:
            Dictionary with 'listenKey' field (valid for 60 minutes)
        """
        return self.client.request("POST", "/openApi/user/auth/userDataStream")

    def extend(self, listen_key: str) -> Dict[str, Any]:
        """
        Extend listen key validity (recommended every 30 minutes)

        Args:
            listen_key: Listen key to extend
        """
        return self.client.request("PUT", "/openApi/user/auth/userDataStream", {"listenKey": listen_key})

    def delete(self, listen_key: str) -> Dict[str, Any]:
        """
        Delete a listen key

        Args:
            listen_key: Listen key to delete
        """
        return self.client.request("DELETE", "/openApi/user/auth/userDataStream", {"listenKey": listen_key})
