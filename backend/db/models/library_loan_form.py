from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship

from db.base_class import Base



class LibraryLoanForm(Base):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(Date, nullable=True)
    created_by = Column(String(50), nullable=True)
    updated_by = Column(String(50), nullable=True)
    name_reader = Column(String(50), nullable=True)

    # book_name = Column(String(50), nullable=True)
    # category = Column(String(50), nullable=False)
    # author = Column(String(50), nullable=False)
    detail_book = Column(JSON, nullable=True)
    owner = Column(String(50), nullable=False)
    