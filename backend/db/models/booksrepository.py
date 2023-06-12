from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKe,  DateTime, func
from sqlalchemy.orm import relationship

from db.base_class import Base


class BookRepository(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    year_of_publication = Column(Date, nullable=False)
    publisher = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(50), nullable=True)
    numbers = Column(Integer, nullable=True)

