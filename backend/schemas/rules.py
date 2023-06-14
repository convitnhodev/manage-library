from typing import Optional, List
from pydantic import BaseModel, EmailStr

class RuleCreate(BaseModel): 
    min_age = int 
    max_age: int 
    time_effective_card: int 
    numbers_category: int 
    detail_category: List[str]
    max_day_borrow: str
    max_items_borrow: str 
    