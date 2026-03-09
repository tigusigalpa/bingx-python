"""
Account Data Stream

WebSocket client for private account data streams.
"""

import json
import threading
from typing import Any, Callable, Dict, List, Optional

import websocket


class AccountDataStream:
    """WebSocket client for account data streams"""

    def __init__(
        self, listen_key: str, base_url: str = "wss://open-api-swap.bingx.com/swap-market"
    ):
        """
        Initialize Account Data Stream

        Args:
            listen_key: Listen key from ListenKeyService
            base_url: WebSocket base URL
        """
        self.listen_key = listen_key
        self.base_url = base_url
        self.ws: Optional[websocket.WebSocketApp] = None
        self.balance_handler: Optional[Callable[[List[Dict[str, Any]]], None]] = None
        self.position_handler: Optional[Callable[[List[Dict[str, Any]]], None]] = None
        self.order_handler: Optional[Callable[[Dict[str, Any]], None]] = None
        self.error_handler: Optional[Callable[[Exception], None]] = None
        self.close_handler: Optional[Callable[[], None]] = None
        self._thread: Optional[threading.Thread] = None

    def connect(self) -> None:
        """Connect to WebSocket"""
        url = f"{self.base_url}?listenKey={self.listen_key}"
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """Handle WebSocket open event"""
        pass

    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            event_type = data.get("e")

            if event_type == "ACCOUNT_UPDATE":
                if "a" in data and "B" in data["a"]:
                    if self.balance_handler:
                        self.balance_handler(data["a"]["B"])
                if "a" in data and "P" in data["a"]:
                    if self.position_handler:
                        self.position_handler(data["a"]["P"])

            elif event_type == "ORDER_TRADE_UPDATE":
                if "o" in data:
                    if self.order_handler:
                        self.order_handler(data["o"])

        except json.JSONDecodeError as e:
            if self.error_handler:
                self.error_handler(e)

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        """Handle WebSocket error"""
        if self.error_handler:
            self.error_handler(error)

    def _on_close(self, ws: websocket.WebSocketApp, close_status_code: int, close_msg: str) -> None:
        """Handle WebSocket close event"""
        if self.close_handler:
            self.close_handler()

    def on_balance_update(self, handler: Callable[[List[Dict[str, Any]]], None]) -> None:
        """
        Set balance update handler

        Args:
            handler: Callback function for balance updates
        """
        self.balance_handler = handler

    def on_position_update(self, handler: Callable[[List[Dict[str, Any]]], None]) -> None:
        """
        Set position update handler

        Args:
            handler: Callback function for position updates
        """
        self.position_handler = handler

    def on_order_update(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Set order update handler

        Args:
            handler: Callback function for order updates
        """
        self.order_handler = handler

    def on_error(self, handler: Callable[[Exception], None]) -> None:
        """
        Set error handler

        Args:
            handler: Callback function for errors
        """
        self.error_handler = handler

    def on_close(self, handler: Callable[[], None]) -> None:
        """
        Set close handler

        Args:
            handler: Callback function for close event
        """
        self.close_handler = handler

    def listen(self) -> None:
        """Start listening for WebSocket messages (blocking)"""
        if self.ws:
            self.ws.run_forever()

    def listen_async(self) -> None:
        """Start listening for WebSocket messages (non-blocking)"""
        if self.ws:
            self._thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self._thread.start()

    def disconnect(self) -> None:
        """Disconnect from WebSocket"""
        if self.ws:
            self.ws.close()
