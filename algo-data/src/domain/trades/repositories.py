from abc import ABC, abstractmethod
from typing import Optional

from src.domain.trades.entities import Trade



class TradeRepository(ABC):
    @abstractmethod
    def save(self, trade: Trade):
        pass

    @abstractmethod
    def get_by_id(self, trade_id: str) -> Optional[Trade]:
        pass

    @abstractmethod
    def list_all(self) -> list[Trade]:
        pass