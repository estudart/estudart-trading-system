import time
import logging

from src.application.data_collectors.data_collector import DataCollector
from src.infrastructure.adapters.websocket_adapter import WebsocketAdapter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter


class OrderReporter(DataCollector):
    def __init__(
        self,
        logger: logging.Logger,
        reporter_adapter: WebsocketAdapter,
        redis_adapter: RedisAdapter
    ):
        self.logger = logger
        self.reporter_adapter = reporter_adapter
        self.redis_adapter = redis_adapter

    def dispatch_order_report_event(self, processed_message_data: dict):
        channel = f"order-{processed_message_data['order_id']}"
        self.redis_adapter.publish_message(channel, processed_message_data)
        self.logger.info(f"{channel} | Order report event was dispatched: {processed_message_data}")

    def start_collecting(self):
        while True:
            try:
                ws = self.reporter_adapter.get_ws(self.dispatch_order_report_event)
                ws.run_forever()
            except Exception:
                self.logger.info("WebSocket disconnected. Reconnecting in 5 seconds...")
                time.sleep(5)

    def run(self):
        self.start_collecting()
