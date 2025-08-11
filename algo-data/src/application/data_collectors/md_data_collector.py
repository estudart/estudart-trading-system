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
        self.from_underlying_to_etf = {
            "BTCUSD_PERP": {
                "onshore": "BITH11",
                "offshore": "HBTC.BH"
            },
            "ETHUSD_PERP": {
                "onshore": "ETHE11",
                "offshore": "HETH.BH"
            },
            "SOLUSD_PERP": {
                "onshore": "SOLH11",
                "offshore": "HSOL.BH"
            },
        }
        self.inav_price_dict = {}

    def should_publish_data(self, symbol, inav):
        if not self.inav_price_dict.get(symbol):
            return True
        
        if inav != self.inav_price_dict[symbol]:
            return True
        
        return False

    def mount_message_data(self, asset: str, inav: float, amount_of_underlying_asset: float):
        return {
            "symbol": asset,
            "inav": inav,
            "amount_of_underlying_asset": amount_of_underlying_asset
        }
    
    def publish_data(self, provider: str, asset: str, price: float):
        onshore = self.from_underlying_to_etf[asset]["onshore"]
        offshore = self.from_underlying_to_etf[asset]["offshore"]

        qty = self.inav_adapter.get_crypto_quantity_on_onshore_etf(onshore, offshore)
        dollar_price = float(self.message_broker.get_key("USD:BRL"))
        inav = round(qty * price * dollar_price, 2)

        if self.should_publish_data(onshore, inav):
            self.inav_price_dict[onshore] = inav
        else:
            return

        channel = f"inav-{onshore}-{provider}"
        self.logger.info(f"{channel}: {inav}")
        message_data = self.mount_message_data(onshore, inav, qty)
        self.message_broker.publish_message(channel, message_data)

    def start_websocket_session(self):
        self.logger.info(f"Starting websocket connection...")
        ws = self.websocket_adapter.get_ws(self.publish_data)
        ws.run_forever()
    
    def start_collecting(self):
        self.logger.info(f"Caching underlying quantity on ETFs...")
        for k, v in self.from_underlying_to_etf.items():
            self.inav_adapter.get_crypto_quantity_on_onshore_etf(v["onshore"], v["offshore"])

        while True:
            try:
                self.start_websocket_session()
            except Exception as err:
                self.logger.exception(f"Websocket session crashed, reason: {err}")
        
            self.logger.info(f"Restarting session in {self.retry_time} seconds...")
            time.sleep(self.retry_time)
    
    def run(self):
        self.start_collecting()
