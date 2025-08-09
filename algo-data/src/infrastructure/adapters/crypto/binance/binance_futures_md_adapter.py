from typing import Callable
import logging
import json
import os

import websocket
from dotenv import load_dotenv

from src.infrastructure.adapters.websocket_adapter import WebsocketAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")


class BinanceCoinMWebsocketAdapter(WebsocketAdapter):
    def __init__(
        self,
        logger: logging.Logger
    ) -> None:
        self.logger = logger
        # Example: ["btcusd_perp@ticker", "ethusd_perp@ticker"]
        self.streams: list = json.loads(os.environ.get(f'BINANCE_COINM_STREAMS_{ENV}'))
        self.host: str = os.environ.get(f'BINANCE_COINM_WSS_HOST_{ENV}')
        self.on_event: Callable = None

    def on_message(self, ws: websocket.WebSocketApp, message):
        try:
            message_json = json.loads(message)
            self.on_event("market-data", message_json)
            self.logger.info(f"Data was streamed: {message_json}")
        except Exception as err:
            self.logger.error(f"Binance Coin-M: Could not process message, reason: {err}")
            
    def on_error(self, ws: websocket.WebSocketApp, error):
        self.logger.error(f"Binance Coin-M: {error}")

    def on_open(self, ws: websocket.WebSocketApp):
        self.logger.info(f"Binance Coin-M: Streams: {self.streams}")
        pass

    def on_close(self, ws, close_status_code, close_msg):
        self.logger.info(f"Binance Coin-M: Connection closed with code: {close_status_code}, message: {close_msg}")

    def get_ws(self, callback: Callable) -> websocket.WebSocketApp:
        websocket.enableTrace(False)
        self.on_event = callback

        stream_path = "/".join(self.streams)
        url = f"{self.host}/stream?streams={stream_path}"

        ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close
        )
        return ws
