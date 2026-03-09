"""
BingX Client

Main client class for interacting with BingX API.
"""

from typing import Optional

from .http.base_client import BaseHTTPClient
from .services import (
    AccountService,
    ContractService,
    CopyTradingService,
    ListenKeyService,
    MarketService,
    SpotAccountService,
    SubAccountService,
    TradeService,
    WalletService,
)
from .coinm_client import CoinMClient


class BingXClient:
    """Main BingX API client"""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_uri: str = "https://open-api.bingx.com",
        source_key: Optional[str] = None,
        signature_encoding: str = "base64",
        timeout: int = 30,
    ):
        """
        Initialize BingX client

        Args:
            api_key: BingX API key
            api_secret: BingX API secret
            base_uri: Base URI for API endpoints
            source_key: Optional source key for tracking
            signature_encoding: Signature encoding method ('base64' or 'hex')
            timeout: Request timeout in seconds
        """
        self.http_client = BaseHTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            base_uri=base_uri,
            source_key=source_key,
            signature_encoding=signature_encoding,
            timeout=timeout,
        )

        self._market = MarketService(self.http_client)
        self._account = AccountService(self.http_client)
        self._trade = TradeService(self.http_client)
        self._contract = ContractService(self.http_client)
        self._listen_key = ListenKeyService(self.http_client)
        self._wallet = WalletService(self.http_client)
        self._spot_account = SpotAccountService(self.http_client)
        self._sub_account = SubAccountService(self.http_client)
        self._copy_trading = CopyTradingService(self.http_client)
        self._coinm_client: Optional[CoinMClient] = None

    def market(self) -> MarketService:
        """Get Market Service for market data operations"""
        return self._market

    def account(self) -> AccountService:
        """Get Account Service for account operations"""
        return self._account

    def trade(self) -> TradeService:
        """Get Trade Service for trading operations"""
        return self._trade

    def contract(self) -> ContractService:
        """Get Contract Service for standard contract operations"""
        return self._contract

    def listen_key(self) -> ListenKeyService:
        """Get Listen Key Service for WebSocket authentication"""
        return self._listen_key

    def wallet(self) -> WalletService:
        """Get Wallet Service for wallet operations (deposits, withdrawals)"""
        return self._wallet

    def spot_account(self) -> SpotAccountService:
        """Get Spot Account Service for spot account operations"""
        return self._spot_account

    def sub_account(self) -> SubAccountService:
        """Get Sub-Account Service for sub-account management operations"""
        return self._sub_account

    def copy_trading(self) -> CopyTradingService:
        """Get Copy Trading Service for copy trading operations"""
        return self._copy_trading

    def coinm(self) -> CoinMClient:
        """
        Get Coin-M Perpetual Futures Client

        Provides access to Coin-Margined perpetual futures API.
        These contracts are margined and settled in cryptocurrency (BTC, ETH, etc.)
        instead of USDT.
        """
        if self._coinm_client is None:
            self._coinm_client = CoinMClient(self.http_client)
        return self._coinm_client

    def get_http_client(self) -> BaseHTTPClient:
        """Get the underlying HTTP client"""
        return self.http_client

    def get_endpoint(self) -> str:
        """Get API endpoint URL"""
        return self.http_client.get_endpoint()

    def get_api_key(self) -> str:
        """Get API key"""
        return self.http_client.get_api_key()
