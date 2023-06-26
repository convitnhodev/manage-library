from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import  Enum
from datetime import datetime



class ListReturn: 
    def __init__(self, data, total: int): 
        self.data = data 
        self.total = total





