from dataclasses import dataclass



@dataclass
class Trade:
    trade_id: str
    order_id: str
    symbol: str
    side: str
    quantity: float
    price: float
    trade_date: str
