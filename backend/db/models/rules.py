from sqlalchemy import Column, Integer, String, Boolean, Date, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db.base_class import Base

class Rule(Base):
    id = Column(Integer, primary_key=True)
    owner = Column(String(50), nullable=True)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    time_effective_card = Column(Integer, nullable=True)
    detail_type = Column(JSON, nullable=True)
    numbers_category = Column(Integer, nullable=True)
    detail_category = Column(JSON, nullable=True)
    distance_year = Column(Integer, nullable=True)
    max_day_borrow = Column(Integer, nullable=True)
    max_items_borrow = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)



