from sqlalchemy import Column, String, Float

from .base import Base



class TradeModel(Base):
    __tablename__ = "trades"

    trade_id = Column(String, primary_key=True, index=True)
    order_id = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    trade_date = Column(String, nullable=False)
