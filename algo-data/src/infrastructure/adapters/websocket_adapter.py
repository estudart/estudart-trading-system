from abc import ABC, abstractmethod

import websocket



class WebsocketAdapter(ABC):
    @abstractmethod
    def get_ws(self) -> websocket.WebSocketApp:
        pass