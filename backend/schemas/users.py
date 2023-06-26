from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    name: Optional[str] 
    address: Optional[str]
    dob: Optional[str]
    email: EmailStr
    password: str 
    numberphone: Optional[str]


class UserShow(BaseModel):
    username: str
    name: str 
    address: str
    dob: str
    email: EmailStr
    numberphone: str 
    class Config(): 
        orm_mode = True 



    

