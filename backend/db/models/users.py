from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

from db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    numberphone = Column(String(50), unique=True)
    name = Column(String(50), nullable=False)
    dob = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(150), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.utcnow() + timedelta(days=90))
    created_by = Column(String(50), default="ADMIN")
    updated_by = Column(String(50), default="ADMIN")
    is_active = Column(Boolean(), nullable=True)
    is_supperuser = Column(Boolean(), default=False)
    owner = Column(String(50))
