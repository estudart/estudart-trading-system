import time
import logging

from src.application.data_collectors.data_collector import DataCollector
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter
from src.infrastructure.adapters.md_adapter import MDAdapter



class DollarCollector(DataCollector):
    def __init__(
            self,
            logger: logging.Logger,
            redis_adapter: RedisAdapter,
            dollar_adapter: MDAdapter
        ):
        self.logger = logger
        self.redis_adapter = redis_adapter
        self.dollar_adapter = dollar_adapter
    
    def collect_dollar(self):
        dollar_price = self.dollar_adapter.fetch_price()
        self.redis_adapter.set_key("USD:BRL", dollar_price)

    def start_collecting(self):
        while True:
            try:
                self.collect_dollar()
            except Exception as err:
                self.logger.error(f"Could not fetch dollar price, reason: {err}")
            time.sleep(5)

    def run(self):
        self.start_collecting()