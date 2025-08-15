from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///src/database/trading-system.db")
SessionLocal = sessionmaker(bind=engine)
