from typing import Optional, List
from pydantic import BaseModel, EmailStr
from enum import  Enum
from datetime import datetime
import json



class DetailBook(BaseModel): 
    ordinal_number: int
    book_name: str 
    category: str 
    author: str 
    number: str 
    def json(self):
        return self.dict()

class LibraryLoanFormModel(BaseModel): 
    detail_book: List[DetailBook]
    created_at: datetime
    updated_at: datetime
    owner: str
    expires_at: datetime
    name_reader: str 


class LibraryLoanFormCreate(BaseModel): 
    detail_book: List[DetailBook]
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    name_reader: str 










