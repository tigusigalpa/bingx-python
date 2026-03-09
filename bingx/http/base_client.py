"""
Base HTTP Client for BingX API

Handles request signing, authentication, and error handling.
"""

import base64
import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from ..exceptions import (
    APIException,
    AuthenticationException,
    BingXException,
    InsufficientBalanceException,
    RateLimitException,
)


class BaseHTTPClient:
    """Base HTTP client for making authenticated requests to BingX API"""

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
        Initialize the HTTP client

        Args:
            api_key: BingX API key
            api_secret: BingX API secret
            base_uri: Base URI for API endpoints
            source_key: Optional source key for tracking
            signature_encoding: Signature encoding method ('base64' or 'hex')
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_uri = base_uri.rstrip("/")
        self.source_key = source_key
        self.signature_encoding = signature_encoding
        self.timeout = timeout
        self.session = requests.Session()

    def _timestamp(self) -> str:
        """Generate current timestamp in milliseconds"""
        return str(int(time.time() * 1000))

    def _build_query(self, params: Dict[str, Any]) -> str:
        """
        Build query string from parameters

        Args:
            params: Dictionary of parameters

        Returns:
            URL-encoded query string
        """
        if not params:
            return ""

        sorted_params = sorted(params.items())
        return urlencode(sorted_params)

    def _sign_string(self, string: str) -> str:
        """
        Sign a string using HMAC-SHA256

        Args:
            string: String to sign

        Returns:
            Signed string (base64 or hex encoded)
        """
        signature = hmac.new(
            self.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256
        ).digest()

        if self.signature_encoding == "hex":
            return signature.hex()

        return base64.b64encode(signature).decode("utf-8")

    def _headers(self) -> Dict[str, str]:
        """
        Build request headers

        Returns:
            Dictionary of headers
        """
        headers = {
            "X-BX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if self.source_key:
            headers["X-SOURCE-KEY"] = self.source_key

        return headers

    def _handle_api_error(self, response: Dict[str, Any]) -> None:
        """
        Handle API-level errors

        Args:
            response: API response dictionary

        Raises:
            APIException or subclass if error detected
        """
        if "code" not in response:
            return

        code = str(response.get("code", ""))
        message = response.get("msg", "Unknown API error")

        if code in ["100001", "100002", "100003", "100004"]:
            raise AuthenticationException(message, response_data=response)
        elif code == "100005":
            raise RateLimitException(message, response_data=response)
        elif code == "200001":
            raise InsufficientBalanceException(message, response_data=response)
        else:
            raise APIException(message, code, response)

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the BingX API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Request parameters
            **kwargs: Additional arguments for requests

        Returns:
            API response as dictionary

        Raises:
            BingXException: On request or API errors
        """
        method = method.upper()
        params = params or {}

        if "timestamp" not in params:
            params["timestamp"] = self._timestamp()

        query = self._build_query(params)
        signature = self._sign_string(query)
        headers = self._headers()

        url = f"{self.base_uri}{path}"

        try:
            if method in ["GET", "DELETE"]:
                params["signature"] = signature
                response = self.session.request(
                    method, url, params=params, headers=headers, timeout=self.timeout, **kwargs
                )
            else:
                params["signature"] = signature
                response = self.session.request(
                    method, url, data=params, headers=headers, timeout=self.timeout, **kwargs
                )

            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                raise BingXException(
                    "Invalid JSON response from API",
                    response_data={"raw": response.text},
                )

            if not isinstance(data, dict):
                raise BingXException(
                    "Invalid response format from API",
                    response_data={"raw": response.text},
                )

            self._handle_api_error(data)

            return data

        except requests.exceptions.RequestException as e:
            response_data = {}
            if hasattr(e, "response") and e.response is not None:
                try:
                    response_data = e.response.json()
                except ValueError:
                    response_data = {"raw": e.response.text}

            raise BingXException(
                f"HTTP request failed: {str(e)}",
                code=e.response.status_code if hasattr(e, "response") else None,
                original_exception=e,
                response_data=response_data,
            )

    def get_endpoint(self) -> str:
        """Get the base API endpoint"""
        return self.base_uri

    def get_api_key(self) -> str:
        """Get the API key"""
        return self.api_key
