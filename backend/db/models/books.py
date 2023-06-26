from sqlalchemy import Column, Integer, String, Boolean, Date, JSON, ForeignKey, DateTime, func

from db.base_class import Base

class Book(Base):
    id = Column(Integer, primary_key=True)
    owner = Column(String(50), nullable=False)
    book_name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    year_of_publication = Column(Integer, nullable=False)
    publisher = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    created_by = Column(String(50), nullable=True)
    updated_by = Column(String(50), nullable=True)
    numbers = Column(Integer, nullable=True)
    amount_borrowed = Column(Integer, nullable=True, default=0)
    #detail_adding_book = Column(JSON, nullable=True)

    





