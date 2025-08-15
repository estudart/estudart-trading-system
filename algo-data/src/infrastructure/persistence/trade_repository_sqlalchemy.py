from typing import Optional, List
from sqlalchemy.orm import Session

from src.domain.trades.entities import Trade
from src.domain.trades.repositories import TradeRepository
from .trade_models import TradeModel



class TradeRepositorySQLAlchemy(TradeRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, trade: Trade) -> None:
        try:
            trade_model = TradeModel(
                trade_id=trade.trade_id,
                order_id=trade.order_id,
                symbol=trade.symbol,
                side=trade.side,
                quantity=trade.quantity,
                price=trade.price,
                trade_date=trade.trade_date
            )
            self.session.add(trade_model)
            self.session.commit()
        except Exception as err:
            self.session.rollback()

    def get_by_id(self, trade_id: str) -> Optional[Trade]:
        model = self.session.query(TradeModel).filter_by(trade_id=trade_id).first()
        if model:
            return Trade(
                trade_id=model.trade_id,
                order_id=model.order_id,
                symbol=model.symbol,
                side=model.side,
                quantity=model.quantity,
                price=model.price,
                trade_date=model.trade_date
            )
        return None

    def list_all(self) -> List[Trade]:
        models = self.session.query(TradeModel).all()
        return [
            Trade(
                order_id=m.order_id,
                trade_id=m.trade_id,
                symbol=m.symbol,
                side=m.side,
                quantity=m.quantity,
                price=m.price,
                trade_date=m.trade_date
            )
            for m in models
        ]
