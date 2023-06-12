from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db.base_class import Base



class BookLoanVoucher(Base):
    id = Column(Integer, primary_key=True)
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(String(50), nullable=False)
    updated_by = Column(String(50), nullable=False)