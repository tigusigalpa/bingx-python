"""
Base HTTP Client for BingX API

Handles request signing, authentication, and error handling.
Implements automatic fallback to .pro domain on network/timeout errors.
"""

import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import requests

from ..exceptions import (
    APIException,
    AuthenticationException,
    BingXException,
    InsufficientBalanceException,
    RateLimitException,
)

DEFAULT_SOURCE_KEY = "BX-AI-SKILL"

BASE_URLS = {
    "prod-live": ["https://open-api.bingx.com", "https://open-api.bingx.pro"],
    "prod-vst": ["https://open-api-vst.bingx.com", "https://open-api-vst.bingx.pro"],
}


class BaseHTTPClient:
    """Base HTTP client for making authenticated requests to BingX API"""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_uri: str = "https://open-api.bingx.com",
        source_key: Optional[str] = None,
        signature_encoding: str = "hex",
        timeout: int = 30,
        enable_fallback: bool = True,
    ):
        """
        Initialize the HTTP client

        Args:
            api_key: BingX API key
            api_secret: BingX API secret
            base_uri: Base URI for API endpoints
            source_key: Source key for tracking (defaults to BX-AI-SKILL)
            signature_encoding: Signature encoding method ('base64' or 'hex', default 'hex')
            timeout: Request timeout in seconds
            enable_fallback: Enable automatic fallback to .pro domain on network errors
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_uri = base_uri.rstrip("/")
        self.source_key = source_key if source_key is not None else DEFAULT_SOURCE_KEY
        self.signature_encoding = signature_encoding
        self.timeout = timeout
        self.enable_fallback = enable_fallback
        self.session = requests.Session()
        
        self._fallback_urls = self._get_fallback_urls()

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

    def _get_fallback_urls(self) -> List[str]:
        """
        Get list of fallback URLs based on base_uri
        
        Returns:
            List of URLs to try (primary first, then fallback)
        """
        for env, urls in BASE_URLS.items():
            if self.base_uri in urls:
                return urls
        return [self.base_uri]

    def _is_network_error(self, exception: Exception) -> bool:
        """
        Check if exception is a network/timeout error that should trigger fallback
        
        Args:
            exception: The exception to check
            
        Returns:
            True if this is a network error that should trigger fallback
        """
        return isinstance(exception, (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout,
        ))

    def _headers(self, content_type: str = "application/x-www-form-urlencoded") -> Dict[str, str]:
        """
        Build request headers

        Args:
            content_type: Content-Type header value

        Returns:
            Dictionary of headers
        """
        headers = {
            "X-BX-APIKEY": self.api_key,
            "Content-Type": content_type,
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

        code = response.get("code")
        
        if code == 0:
            return
        
        code_str = str(code)
        message = response.get("msg", "Unknown API error")

        if code_str in ["100001", "100002", "100003", "100004"]:
            raise AuthenticationException(message, response_data=response)
        elif code_str == "100005":
            raise RateLimitException(message, response_data=response)
        elif code_str == "200001":
            raise InsufficientBalanceException(message, response_data=response)
        elif code_str != "0":
            raise APIException(message, code_str, response)

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body_type: str = "form",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the BingX API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Request parameters
            body_type: Body encoding type ('form' or 'json')
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

        urls_to_try = self._fallback_urls if self.enable_fallback else [self.base_uri]
        last_exception = None

        for base_url in urls_to_try:
            try:
                return self._execute_request(method, base_url, path, params, body_type, **kwargs)
            except requests.exceptions.RequestException as e:
                last_exception = e
                if not self.enable_fallback or not self._is_network_error(e):
                    raise self._wrap_request_exception(e)
                continue

        if last_exception:
            raise self._wrap_request_exception(last_exception)

    def _execute_request(
        self,
        method: str,
        base_url: str,
        path: str,
        params: Dict[str, Any],
        body_type: str = "form",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Execute a single request to a specific URL
        
        Args:
            method: HTTP method
            base_url: Base URL to use
            path: API endpoint path
            params: Request parameters
            body_type: Body encoding type ('form' or 'json')
            **kwargs: Additional arguments for requests
            
        Returns:
            API response as dictionary
        """
        query = self._build_query(params)
        signature = self._sign_string(query)
        
        url = f"{base_url}{path}"

        if method in ["GET", "DELETE"]:
            headers = self._headers()
            params_with_sig = {**params, "signature": signature}
            response = self.session.request(
                method, url, params=params_with_sig, headers=headers, timeout=self.timeout, **kwargs
            )
        else:
            if body_type == "json":
                headers = self._headers("application/json")
                body_data = {**params, "signature": signature}
                response = self.session.request(
                    method, url, json=body_data, headers=headers, timeout=self.timeout, **kwargs
                )
            else:
                headers = self._headers()
                params_with_sig = {**params, "signature": signature}
                response = self.session.request(
                    method, url, data=params_with_sig, headers=headers, timeout=self.timeout, **kwargs
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

    def _wrap_request_exception(self, e: requests.exceptions.RequestException) -> BingXException:
        """
        Wrap a requests exception in a BingXException
        
        Args:
            e: The original exception
            
        Returns:
            BingXException wrapping the original error
        """
        response_data = {}
        if hasattr(e, "response") and e.response is not None:
            try:
                response_data = e.response.json()
            except ValueError:
                response_data = {"raw": e.response.text}

        return BingXException(
            f"HTTP request failed: {str(e)}",
            code=e.response.status_code if hasattr(e, "response") and e.response else None,
            original_exception=e,
            response_data=response_data,
        )

    def get_endpoint(self) -> str:
        """Get the base API endpoint"""
        return self.base_uri

    def get_api_key(self) -> str:
        """Get the API key"""
        return self.api_key
