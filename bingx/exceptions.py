"""
BingX API Exceptions

Custom exception classes for handling BingX API errors.
"""

from typing import Any, Dict, Optional


class BingXException(Exception):
    """Base exception for all BingX errors"""

    def __init__(
        self,
        message: str,
        code: Optional[int] = None,
        original_exception: Optional[Exception] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.original_exception = original_exception
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class APIException(BingXException):
    """Exception for API-level errors"""

    def __init__(self, message: str, code: str, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message, None, None, response_data)
        self.api_code = code

    def __str__(self) -> str:
        return f"[API Error {self.api_code}] {self.message}"


class AuthenticationException(BingXException):
    """Exception for authentication errors (invalid API key/secret)"""

    pass


class RateLimitException(BingXException):
    """Exception for rate limit errors"""

    pass


class InsufficientBalanceException(BingXException):
    """Exception for insufficient balance errors"""

    pass
