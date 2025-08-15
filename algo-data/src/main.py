from multiprocessing import Process
import time

from src.application.data_collectors import (
    InavDataCollector,
    OrderReporter,
    TradeStreamer,
    MdDataCollector,
    DollarCollector
)
from src.application.data_consumers import (
    DataConsumer,
    FlowaDataConsumer
)
from src.infrastructure.adapters.crypto.coinbase.coinbase_dollar_adapter import CoinbaseDollarAdapter
from src.infrastructure.adapters.stocks.hashdex.hashdex_md_adapter import HashdexMDAdapter
from src.infrastructure.adapters.stocks.flowa.flowa_trade_reporter import FlowaTradeReporter
from src.infrastructure.adapters.crypto.binance.binance_futures_md_adapter import BinanceCoinMWebsocketAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter
from src.infrastructure.persistence.trade_repository_sqlalchemy import TradeRepositorySQLAlchemy
from src.infrastructure.persistence.base import Base, engine, SessionLocal



def start_inav_collector_process(logger):
    inav_collector = InavDataCollector(
        logger=logger,
        collector_adapter=HashdexMDAdapter(logger),
        redis_adapter=RedisAdapter(logger),
        assets_list=["BITH11", "ETHE11", "SOLH11"]
    )
    inav_collector.run()

def start_dollar_collector_process(logger):
    dollar_collector = DollarCollector(
        logger=logger,
        redis_adapter=RedisAdapter(logger),
        dollar_adapter=CoinbaseDollarAdapter(logger)
    )
    dollar_collector.run()

def start_binance_md_collector(logger):
    binance_md_collector = MdDataCollector(
        logger=logger,
        websocket_adapter=BinanceCoinMWebsocketAdapter(logger),
        inav_adapter=HashdexMDAdapter(logger),
        message_broker=RedisAdapter(logger),
        retry_time=2
    )
    binance_md_collector.run()

def start_order_reporter_process(logger):
    order_reporter = OrderReporter(
        logger=logger,
        reporter_adapter=FlowaTradeReporter(
            channel="orders",
            logger=logger
        ),
        redis_adapter=RedisAdapter(logger)
    )
    order_reporter.run()

def start_trade_streamer_process(logger):
    trade_streamer = TradeStreamer(
        logger=logger,
        reporter_adapter=FlowaTradeReporter(
            channel="trades",
            logger=logger
        ),
        redis_adapter=RedisAdapter(logger),
        provider="Flowa"
    )
    trade_streamer.run()

def start_trade_consumer_process(logger):
    trade_consumer = FlowaDataConsumer(
        logger=logger,
        message_boker=RedisAdapter(
            logger=logger
        ),
        trade_repository=TradeRepositorySQLAlchemy(
            session=SessionLocal()
        )
    )
    trade_consumer.run()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    logger = LoggerAdapter().get_logger()

    process_list: list[Process] = [
        Process(target=start_trade_consumer_process, args=(logger, )),
        Process(target=start_trade_streamer_process, args=(logger, )),
        Process(target=start_dollar_collector_process, args=(logger, )),
        Process(target=start_order_reporter_process, args=(logger, )),
        Process(target=start_binance_md_collector, args=(logger, )),
    ]

    try:
        for p in process_list:
            p.start()
            time.sleep(5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Terminating child processes...")

        for p in process_list:
            p.terminate()
        
        for p in process_list:
            p.join()
        
        print("All processes terminated.")
