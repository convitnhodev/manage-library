from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    name: str 
    address: str
    dob: str
    email: EmailStr
    password: str 
    numberphone: str 


class UserShow(BaseModel):
    username: str
    name: str 
    address: str
    dob: str
    email: EmailStr
    numberphone: str 
    class Config(): 
        orm_mode = True 



    

