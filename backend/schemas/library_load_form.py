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
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    owner: Optional[str]
    expires_at: Optional[datetime]
    name_reader: str 


class LibraryLoanFormCreate(BaseModel): 
    detail_book: List[DetailBook]
    name_reader: str 

class LibraryLoanFormCreate(BaseModel): 
    id_card: int 
    ids_books: List[int]
    created_at: Optional[datetime]










