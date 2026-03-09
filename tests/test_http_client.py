"""
Tests for HTTP Client

Tests for the base HTTP client functionality.
"""

import pytest
from bingx.http.base_client import BaseHTTPClient


def test_http_client_initialization():
    """Test HTTP client initialization"""
    client = BaseHTTPClient(
        api_key="test_key",
        api_secret="test_secret"
    )
    
    assert client.api_key == "test_key"
    assert client.api_secret == "test_secret"
    assert client.base_uri == "https://open-api.bingx.com"
    assert client.signature_encoding == "base64"


def test_timestamp_generation():
    """Test timestamp generation"""
    client = BaseHTTPClient(
        api_key="test_key",
        api_secret="test_secret"
    )
    
    timestamp = client._timestamp()
    assert isinstance(timestamp, str)
    assert len(timestamp) == 13  # Millisecond timestamp


def test_build_query():
    """Test query string building"""
    client = BaseHTTPClient(
        api_key="test_key",
        api_secret="test_secret"
    )
    
    params = {"symbol": "BTC-USDT", "limit": 10, "timestamp": "1234567890"}
    query = client._build_query(params)
    
    # Should be sorted alphabetically
    assert "limit=10" in query
    assert "symbol=BTC-USDT" in query
    assert "timestamp=1234567890" in query


def test_sign_string_base64():
    """Test string signing with base64 encoding"""
    client = BaseHTTPClient(
        api_key="test_key",
        api_secret="test_secret",
        signature_encoding="base64"
    )
    
    test_string = "symbol=BTC-USDT&timestamp=1234567890"
    signature = client._sign_string(test_string)
    
    assert isinstance(signature, str)
    assert len(signature) > 0


def test_sign_string_hex():
    """Test string signing with hex encoding"""
    client = BaseHTTPClient(
        api_key="test_key",
        api_secret="test_secret",
        signature_encoding="hex"
    )
    
    test_string = "symbol=BTC-USDT&timestamp=1234567890"
    signature = client._sign_string(test_string)
    
    assert isinstance(signature, str)
    assert len(signature) == 64  # SHA256 hex is 64 characters


def test_headers():
    """Test header generation"""
    client = BaseHTTPClient(
        api_key="test_key",
        api_secret="test_secret"
    )
    
    headers = client._headers()
    
    assert headers["X-BX-APIKEY"] == "test_key"
    assert headers["Content-Type"] == "application/x-www-form-urlencoded"


def test_headers_with_source_key():
    """Test header generation with source key"""
    client = BaseHTTPClient(
        api_key="test_key",
        api_secret="test_secret",
        source_key="source_123"
    )
    
    headers = client._headers()
    
    assert headers["X-SOURCE-KEY"] == "source_123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
