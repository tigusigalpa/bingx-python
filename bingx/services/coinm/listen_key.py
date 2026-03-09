"""
Coin-M Listen Key Service

Handles WebSocket authentication listen keys for Coin-M futures.
"""

from typing import Any, Dict

from ...http.base_client import BaseHTTPClient


class CoinMListenKeyService:
    """Service for Coin-M WebSocket listen key management"""

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Coin-M Listen Key Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def generate(self) -> Dict[str, Any]:
        """
        Generate a new Coin-M listen key

        Returns:
            Dictionary with 'listenKey' field (valid for 60 minutes)
        """
        return self.client.request("POST", "/openApi/cswap/v1/user/auth/userDataStream")

    def extend(self, listen_key: str) -> Dict[str, Any]:
        """
        Extend Coin-M listen key validity (recommended every 30 minutes)

        Args:
            listen_key: Listen key to extend
        """
        return self.client.request(
            "PUT", "/openApi/cswap/v1/user/auth/userDataStream", {"listenKey": listen_key}
        )

    def delete(self, listen_key: str) -> Dict[str, Any]:
        """
        Delete a Coin-M listen key

        Args:
            listen_key: Listen key to delete
        """
        return self.client.request(
            "DELETE", "/openApi/cswap/v1/user/auth/userDataStream", {"listenKey": listen_key}
        )
