from typing import Optional
from pydantic import BaseModel, EmailStr

class CardCreate(BaseModel): 
    name: str 
    type: str 
    dob: str
    address: str
    email: EmailStr
    

