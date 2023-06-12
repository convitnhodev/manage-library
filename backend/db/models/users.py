from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    dob = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(Date, nullable=False)
    created_by = Column(String(50), nullable=False)
    updated_by = Column(String(50), nullable=False)
    is_active = Column(Boolean(), nullable=True)
    is_supperuser = Column(Boolean(), default=False)
