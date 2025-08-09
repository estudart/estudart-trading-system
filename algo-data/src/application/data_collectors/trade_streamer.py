import time
import logging

from src.application.data_collectors.data_collector import DataCollector
from src.infrastructure.adapters.websocket_adapter import WebsocketAdapter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter


class TradeStreamer(DataCollector):
    def __init__(
        self,
        logger: logging.Logger,
        reporter_adapter: WebsocketAdapter,
        redis_adapter: RedisAdapter,
        provider: str
    ):
        self.logger = logger
        self.reporter_adapter = reporter_adapter
        self.redis_adapter = redis_adapter
        self.provider = provider

    def dispatch_trade_report_event(self, message_data: dict):
        channel = f"{self.provider}-trade-{message_data['StrategyID']}"
        self.redis_adapter.stream_data(channel, message_data)
        self.logger.info(f"{channel} | Trade was streammed: {message_data}")

    def start_collecting(self):
        while True:
            try:
                ws = self.reporter_adapter.get_ws(self.dispatch_trade_report_event)
                ws.run_forever()
            except Exception:
                self.logger.info("WebSocket disconnected. Reconnecting in 5 seconds...")
                time.sleep(5)

    def run(self):
        self.start_collecting()
