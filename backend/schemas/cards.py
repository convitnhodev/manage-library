from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import  Enum
from datetime import datetime

class TypeCard(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class CardCreate(BaseModel): 
    age: int
    name: str 
    type: TypeCard
    dob: datetime
    address: str
    email: EmailStr
    

