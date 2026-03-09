"""Service modules for BingX API endpoints"""

from .market import MarketService
from .account import AccountService
from .trade import TradeService
from .wallet import WalletService
from .spot_account import SpotAccountService
from .contract import ContractService
from .listen_key import ListenKeyService
from .sub_account import SubAccountService
from .copy_trading import CopyTradingService

__all__ = [
    "MarketService",
    "AccountService",
    "TradeService",
    "WalletService",
    "SpotAccountService",
    "ContractService",
    "ListenKeyService",
    "SubAccountService",
    "CopyTradingService",
]
