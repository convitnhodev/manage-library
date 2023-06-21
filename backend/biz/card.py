from schemas.cards import CardCreate
from db.models.rules import Rule
from db.repository.rules import get_rule_by_owner
from sqlalchemy.orm import Session
from datetime import date
import json 

def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year

    # Kiểm tra nếu chưa đến ngày sinh trong năm hiện tại
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1

    return age


def is_card_valid(card: CardCreate, owner: str, db: Session): 
    rule = get_rule_by_owner(owner, db)
    if rule is None:
        return True
    if calculate_age(card.dob) < rule.min_age or calculate_age(card.dob) > rule.max_age : 
        return "Age is invalid"
    
    if card.type not in json.loads(rule.detail_type):
        #raise ValueError("Type is invalid")
        return "Type is invalid"
    
    return True