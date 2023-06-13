from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import  Enum

class TypeCard(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class CardCreate(BaseModel): 
    name: str 
    type: TypeCard
    dob: str
    address: str
    email: EmailStr
    

