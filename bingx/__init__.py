"""
BingX Python SDK

Python client for the BingX cryptocurrency exchange API.
Supports USDT-M and Coin-M perpetual futures, spot trading, copy trading, 
sub-accounts, WebSocket streaming.
"""

from .client import BingXClient
from .coinm_client import CoinMClient
from .exceptions import (
    BingXException,
    APIException,
    AuthenticationException,
    RateLimitException,
    InsufficientBalanceException,
)

__version__ = "2.1.7"
__author__ = "Igor Sazonov"
__email__ = "sovletig@gmail.com"

__all__ = [
    "BingXClient",
    "CoinMClient",
    "BingXException",
    "APIException",
    "AuthenticationException",
    "RateLimitException",
    "InsufficientBalanceException",
]
