from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import  Enum
from datetime import datetime

class TypeCard(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class CardCreate(BaseModel): 
    name: str 
    type: str
    dob: datetime
    address: str
    email: EmailStr
    created_at: Optional[datetime]

class CardModel(BaseModel): 
    name: str 
    type: str
    dob: datetime
    address: str
    email: EmailStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    owner: Optional[str]
    expires_at: Optional[datetime]

    





