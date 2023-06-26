from typing import Optional, List
from pydantic import BaseModel, EmailStr
from enum import  Enum
from datetime import datetime
import json



class DetailAddingBook(BaseModel): 
    book_name: str 
    category: str 
    author: str 
    year_of_publication: int 
    publisher: str 
    numbers: int 
    owner: Optional[str]
    amount_borrowed: Optional[int]

    def json(self):
        return self.dict()

class BookModel(BaseModel): 
    detail_adding_book: List[DetailAddingBook]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    owner: Optional[str]
    #expires_at: Optional[datetime]
    id: Optional[str]


class BookCreate(BaseModel): 
    detail_adding_book: List[DetailAddingBook]










