import logging

from src.application.data_consumers.data_consumer import DataConsumer
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter
from src.domain.trades.repositories import TradeRepository
from src.domain.trades.entities import Trade



class FlowaDataConsumer(DataConsumer):
    def __init__(
            self,
            logger: logging.Logger,
            message_boker: RedisAdapter,
            trade_repository: TradeRepository
        ):
        self.logger = logger
        self.message_broker = message_boker
        self.trade_repository = trade_repository
        self.provider = "Flowa"
    
    def consume_data(self, entry_id: str, data: dict):
        try:
            decoded_data = {key.decode('utf-8'): value.decode("utf-8") for key, value in data.items()}
            self.logger.info(f"Consumed new trade: {entry_id}: {decoded_data}")
            self.trade_repository.save(Trade(**decoded_data))
        except Exception as err:
            self.logger.error(f"Could not consume data, reason: {err}")
        
    def run(self):
        self.message_broker.read_stream(f"{self.provider}-trades", self.consume_data)