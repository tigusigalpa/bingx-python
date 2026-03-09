"""
Coin-M Client

Client for Coin-M perpetual futures (crypto-margined contracts).
"""

from .http.base_client import BaseHTTPClient
from .services.coinm import CoinMMarketService, CoinMTradeService, CoinMListenKeyService


class CoinMClient:
    """Client for Coin-M perpetual futures API"""

    def __init__(self, http_client: BaseHTTPClient):
        """
        Initialize Coin-M Client

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client
        self._market = CoinMMarketService(http_client)
        self._trade = CoinMTradeService(http_client)
        self._listen_key = CoinMListenKeyService(http_client)

    def market(self) -> CoinMMarketService:
        """Get Coin-M Market Service"""
        return self._market

    def trade(self) -> CoinMTradeService:
        """Get Coin-M Trade Service"""
        return self._trade

    def listen_key(self) -> CoinMListenKeyService:
        """Get Coin-M Listen Key Service"""
        return self._listen_key
