from sqlalchemy import Column, Integer, String, Boolean, Date, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db.base_class import Base

class Rule(Base):
    id = Column(String(50), primary_key=True)
    owner = Column(String(50), nullable=True)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    time_effective_card = Column(Integer, nullable=False)
    numbers_category = Column(Integer, nullable=False)
    detail_category = Column(JSON, nullable=False)
    max_day_borrow = Column(Integer, nullable=False)
    max_items_borrow = Column(Integer, nullable=False)



