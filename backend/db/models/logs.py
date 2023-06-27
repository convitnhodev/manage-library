from sqlalchemy import Column, Integer, String, Boolean, Date, JSON, ForeignKey, DateTime, func

from db.base_class import Base

class Log(Base):
    id = Column(Integer, primary_key=True)
    owner = Column(String(50), nullable=True)
    action = Column(String(50), nullable=False)
    actor = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
