"""
Tests for Exceptions

Tests for custom exception classes.
"""

import pytest
from bingx.exceptions import (
    BingXException,
    APIException,
    AuthenticationException,
    RateLimitException,
    InsufficientBalanceException,
)


def test_bingx_exception():
    """Test base BingX exception"""
    exc = BingXException("Test error", code=500)
    
    assert str(exc) == "[500] Test error"
    assert exc.code == 500
    assert exc.message == "Test error"


def test_bingx_exception_without_code():
    """Test BingX exception without code"""
    exc = BingXException("Test error")
    
    assert str(exc) == "Test error"
    assert exc.code is None


def test_api_exception():
    """Test API exception"""
    exc = APIException("API error", "100001", {"msg": "Invalid API key"})
    
    assert "API Error 100001" in str(exc)
    assert exc.api_code == "100001"
    assert exc.response_data["msg"] == "Invalid API key"


def test_authentication_exception():
    """Test authentication exception"""
    exc = AuthenticationException("Invalid credentials")
    
    assert str(exc) == "Invalid credentials"
    assert isinstance(exc, BingXException)


def test_rate_limit_exception():
    """Test rate limit exception"""
    exc = RateLimitException("Rate limit exceeded")
    
    assert str(exc) == "Rate limit exceeded"
    assert isinstance(exc, BingXException)


def test_insufficient_balance_exception():
    """Test insufficient balance exception"""
    exc = InsufficientBalanceException("Insufficient balance")
    
    assert str(exc) == "Insufficient balance"
    assert isinstance(exc, BingXException)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
