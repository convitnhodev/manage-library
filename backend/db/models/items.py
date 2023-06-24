from sqlalchemy import Column, Integer, String, Boolean, Date, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db.base_class import Base

class Item(Base):
    id = Column(String(50), primary_key=True)
    owner = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    year_of_publication = Column(Integer, nullable=False)
    publisher = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(50), nullable=True)
    updated_by = Column(String(50), nullable=True)
    numbers = Column(Integer, nullable=True)
    





