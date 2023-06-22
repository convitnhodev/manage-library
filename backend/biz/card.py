from schemas.cards import CardCreate, CardModel
from db.models.rules import Rule
from db.repository.rules import get_rule_by_owner
from db.repository.cards import create_new_card
from sqlalchemy.orm import Session
from datetime import date, datetime
import json 
from const import detail_error as err



def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year

    # Kiểm tra nếu chưa đến ngày sinh trong năm hiện tại
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1

    return age


def is_card_valid(card: CardCreate, rule: Rule): 
    if rule is None:
        return err.CODE_VALID
    if calculate_age(card.dob) < rule.min_age or calculate_age(card.dob) > rule.max_age : 
        return err.CODE_INVALID_AGE
    
    if card.type not in json.loads(rule.detail_type):
        #raise ValueError("Type is invalid")
        return err.CODE_INVALID_TYPE
    return err.CODE_VALID

def user_create_new_card(card: CardCreate, db: Session, owner: str): 
    rule = get_rule_by_owner(owner, db)
    code = is_card_valid(card=card, rule=rule)
    if code != err.CODE_VALID:
        raise code
    
    current_time = datetime.now()
    time_effective_card = rule.time_effective_card
    expire = current_time + datetime.timedelta(seconds=time_effective_card)
    card = CardModel(**card.dict())
    card.owner = owner
    card.expires_at = expire
    create_new_card(card, db)



