from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date

class RuleBase(BaseModel):
    min_age: Optional[int] = 0
    max_age: Optional[int] = 100
    time_effective_card: Optional[int] = 100000
    numbers_category: Optional[int] = 0
    detail_category: List[str] = None
    max_day_borrow: Optional[int] = 100
    max_items_borrow: Optional[int] = 100
    created_at: Optional[date] = datetime.now().date()


class RuleCreate(RuleBase): 
    min_age: int
    max_age: int 
    time_effective_card: int 
    numbers_category: int 
    detail_category: List[str]
    max_day_borrow: int
    max_items_borrow: int 

    