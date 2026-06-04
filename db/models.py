from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from db.database import Base

class DimBank(Base):
    __tablename__ = 'dim_bank'

    bank_code = Column(String(10), primary_key=True, index=True)
    bank_name = Column(String(100), nullable=False)
    bank_type = Column(String(50))
class FactExchangeRate(Base):
    __tablename__ = 'fact_exchange_rate'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_code = Column(String(10), nullable=False)
    
    # Nới rộng từ 3 lên 20 ký tự để khớp với SQL
    currency_code = Column(String(20), nullable=False) 
    
    # THÊM CỘT MỚI Ở ĐÂY
    currency_standard = Column(String(3), nullable=True) 
    
    buy_cash = Column(Numeric(15, 2))
    buy_transfer = Column(Numeric(15, 2))
    sell = Column(Numeric(15, 2))
    record_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (UniqueConstraint('bank_code', 'currency_code', 'record_date', name='uq_exchange_rate'),)