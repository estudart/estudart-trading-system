import time
import logging

from src.infrastructure.adapters.websocket_adapter import WebsocketAdapter
from src.infrastructure.adapters.stocks.hashdex.hashdex_md_adapter import HashdexMDAdapter
from src.application.data_collectors.data_collector import DataCollector
from src.infrastructure.adapters.queue import RedisAdapter



class MdDataCollector(DataCollector):
    def __init__(
            self,
            logger: logging.Logger,
            websocket_adapter: WebsocketAdapter,
            inav_adapter: HashdexMDAdapter,
            message_broker: RedisAdapter,
            retry_time: int
        ):
        self.logger = logger
        self.websocket_adapter = websocket_adapter
        self.inav_adapter = inav_adapter
        self.message_broker = message_broker
        self.retry_time = retry_time
        self.onshore_offshore_mapping = {
            "BITH11": {
                "offshore": "HBTC.BH",
                "underlying_asset": "BTCUSD_PERP"
            },
            "ETHE11": {
                "offshore": "HETH.BH",
                "underlying_asset": "ETHUSD_PERP"
            },
            "SOLH11": {
                "offshore": "HSOL.BH",
                "underlying_asset": "SOLUSD_PERP"
            }
        }
        self.from_underlying_to_etf = {
            "BTCUSD_PERP": "BITH11",
            "ETHUSD_PERP": "ETHE11",
            "SOLUSD_PERP": "SOLH11"
        }
    
    def stream_data(self, provider: str, asset: str, price: float):
        onshore = self.from_underlying_to_etf[asset]
        offshore = self.onshore_offshore_mapping[onshore]["offshore"]
        qty = self.inav_adapter.get_crypto_quantity_on_onshore_etf(onshore, offshore)
        inav = qty * price
        self.logger.info(f"New inav {provider} {asset}: {inav}")
        channel = f"inav-{onshore}-{provider}"
        self.message_broker.publish_message(channel, inav)

    def start_websocket_session(self):
        self.logger.info(f"Starting websocket connection...")
        ws = self.websocket_adapter.get_ws(self.stream_data)
        ws.run_forever()
    
    def start_collecting(self):
        for k, v in self.onshore_offshore_mapping.items():
            self.logger.info(f"Caching underlying quantity on ETFs...")
            self.inav_adapter.get_crypto_quantity_on_onshore_etf(k, v["offshore"])

        while True:
            try:
                self.start_websocket_session()
            except Exception as err:
                self.logger.exception(f"Websocket session crashed, reason: {err}")
        
            self.logger.info(f"Restarting session in {self.retry_time} seconds...")
            time.sleep(self.retry_time)
    
    def run(self):
        self.start_collecting()