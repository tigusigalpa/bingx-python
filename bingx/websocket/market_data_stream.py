"""
Market Data Stream

WebSocket client for public market data streams.
"""

import json
import threading
from typing import Any, Callable, Dict, Optional

import websocket


class MarketDataStream:
    """WebSocket client for market data streams"""

    def __init__(self, base_url: str = "wss://open-api-swap.bingx.com/swap-market"):
        """
        Initialize Market Data Stream

        Args:
            base_url: WebSocket base URL
        """
        self.base_url = base_url
        self.ws: Optional[websocket.WebSocketApp] = None
        self.subscriptions = []
        self.message_handler: Optional[Callable[[Dict[str, Any]], None]] = None
        self.error_handler: Optional[Callable[[Exception], None]] = None
        self.close_handler: Optional[Callable[[], None]] = None
        self._thread: Optional[threading.Thread] = None

    def connect(self) -> None:
        """Connect to WebSocket"""
        self.ws = websocket.WebSocketApp(
            self.base_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """Handle WebSocket open event"""
        for subscription in self.subscriptions:
            ws.send(json.dumps(subscription))

    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            if self.message_handler:
                self.message_handler(data)
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

    def subscribe_trade(self, symbol: str) -> None:
        """
        Subscribe to trade stream

        Args:
            symbol: Trading symbol (e.g., 'BTC-USDT')
        """
        subscription = {"id": f"{symbol}@trade", "dataType": f"{symbol}@trade"}
        self.subscriptions.append(subscription)
        if self.ws:
            self.ws.send(json.dumps(subscription))

    def subscribe_kline(self, symbol: str, interval: str) -> None:
        """
        Subscribe to kline/candlestick stream

        Args:
            symbol: Trading symbol
            interval: Kline interval (1m, 5m, 15m, 30m, 1h, 4h, 1d, etc.)
        """
        subscription = {
            "id": f"{symbol}@kline_{interval}",
            "dataType": f"{symbol}@kline_{interval}",
        }
        self.subscriptions.append(subscription)
        if self.ws:
            self.ws.send(json.dumps(subscription))

    def subscribe_depth(self, symbol: str, limit: int = 20) -> None:
        """
        Subscribe to depth/order book stream

        Args:
            symbol: Trading symbol
            limit: Depth limit (5, 10, 20)
        """
        subscription = {
            "id": f"{symbol}@depth{limit}",
            "dataType": f"{symbol}@depth{limit}",
        }
        self.subscriptions.append(subscription)
        if self.ws:
            self.ws.send(json.dumps(subscription))

    def subscribe_ticker(self, symbol: str) -> None:
        """
        Subscribe to 24hr ticker stream

        Args:
            symbol: Trading symbol
        """
        subscription = {"id": f"{symbol}@ticker", "dataType": f"{symbol}@ticker"}
        self.subscriptions.append(subscription)
        if self.ws:
            self.ws.send(json.dumps(subscription))

    def subscribe_book_ticker(self, symbol: str) -> None:
        """
        Subscribe to best bid/ask stream

        Args:
            symbol: Trading symbol
        """
        subscription = {
            "id": f"{symbol}@bookTicker",
            "dataType": f"{symbol}@bookTicker",
        }
        self.subscriptions.append(subscription)
        if self.ws:
            self.ws.send(json.dumps(subscription))

    def unsubscribe_trade(self, symbol: str) -> None:
        """Unsubscribe from trade stream"""
        unsubscribe = {"id": f"{symbol}@trade", "dataType": f"{symbol}@trade", "unsubscribe": True}
        if self.ws:
            self.ws.send(json.dumps(unsubscribe))

    def unsubscribe_kline(self, symbol: str, interval: str) -> None:
        """Unsubscribe from kline stream"""
        unsubscribe = {
            "id": f"{symbol}@kline_{interval}",
            "dataType": f"{symbol}@kline_{interval}",
            "unsubscribe": True,
        }
        if self.ws:
            self.ws.send(json.dumps(unsubscribe))

    def on_message(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Set message handler

        Args:
            handler: Callback function for messages
        """
        self.message_handler = handler

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
