"""
Tests for BingX Client

Basic tests for the main client class.
"""

import pytest
from bingx import BingXClient
from bingx.exceptions import BingXException


def test_client_initialization():
    """Test client initialization"""
    client = BingXClient(
        api_key="test_key",
        api_secret="test_secret"
    )
    
    assert client.get_api_key() == "test_key"
    assert client.get_endpoint() == "https://open-api.bingx.com"


def test_client_custom_endpoint():
    """Test client with custom endpoint"""
    client = BingXClient(
        api_key="test_key",
        api_secret="test_secret",
        base_uri="https://custom-api.example.com"
    )
    
    assert client.get_endpoint() == "https://custom-api.example.com"


def test_client_services():
    """Test that all services are accessible"""
    client = BingXClient(
        api_key="test_key",
        api_secret="test_secret"
    )
    
    assert client.market() is not None
    assert client.account() is not None
    assert client.trade() is not None
    assert client.wallet() is not None
    assert client.spot_account() is not None
    assert client.sub_account() is not None
    assert client.copy_trading() is not None
    assert client.contract() is not None
    assert client.listen_key() is not None
    assert client.coinm() is not None


def test_signature_encoding():
    """Test different signature encoding methods"""
    client_base64 = BingXClient(
        api_key="test_key",
        api_secret="test_secret",
        signature_encoding="base64"
    )
    
    client_hex = BingXClient(
        api_key="test_key",
        api_secret="test_secret",
        signature_encoding="hex"
    )
    
    assert client_base64.http_client.signature_encoding == "base64"
    assert client_hex.http_client.signature_encoding == "hex"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
