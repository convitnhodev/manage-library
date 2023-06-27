from schemas.cards import CardCreate, CardModel
from db.models.rules import Rule
from db.repository.rules import list_rule_by_owner
from db.repository.cards import create_new_card
from db.repository.cards import list_card_by_owner
from db.repository.cards import get_card_by_id_and_owner
from db.repository.cards import delete_card_by_id_and_owner
from db.repository.cards import update_card_by_id
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
import json 
from const import detail_error 
from const import default
from db.repository.logs import create_log
import threading
from biz.log import log_task


def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year

    # Kiểm tra nếu chưa đến ngày sinh trong năm hiện tại
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1

    return age


def is_card_valid(card: CardCreate, rule: Rule): 
    if rule is None:
        return detail_error.CODE_VALID
    if calculate_age(card.dob) < rule.min_age or calculate_age(card.dob) > rule.max_age : 
        return detail_error.CODE_INVALID_AGE
    
    if card.type not in json.loads(rule.detail_type):
        #raise ValueError("Type is invalid")
        return detail_error.CODE_INVALID_TYPE
    return detail_error.CODE_VALID





def user_create_new_card(card: CardCreate, db: Session, owner: str): 
    rules = list_rule_by_owner(owner, db)
    if len(rules) == 0:
        rule = None
    else :
        rule = rules[0]
    code = is_card_valid(card=card, rule=rule)
    if code != detail_error.CODE_VALID:
        return code
    
    current_time = card.created_at
    if card.created_at is None: 
        current_time = datetime.now()
    if rule is not None:
        time_effective_card = rule.time_effective_card
    else : 
        time_effective_card = default.TIME_EXPIRATION__CARD
    expire = current_time + timedelta(days=time_effective_card)
    card = CardModel(**card.dict())
    card.owner = owner
    card.expires_at = expire
    card = create_new_card(card, db)
    # try: 
    #     log =create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_CREATE_CARD, db=db)
    # except: 
    #     return card


    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_CREATE_CARD, db))
    log_thread.start()
    return card


def user_update_card(card: CardCreate, db: Session, owner: str, id: int):
    rules = list_rule_by_owner(owner, db)
    if len(rules) == 0:
        rule = None
    else :
        rule = rules[0]
    code = is_card_valid(card=card, rule=rule)
    if code != detail_error.CODE_VALID:
        return code
    
    # current_time = datetime.now()
    # if rule is not None:
    #     time_effective_card = rule.time_effective_card
    # else : 
    #     time_effective_card = default.TIME_EXPIRATION_CARD
    # expire = current_time + timedelta(days=time_effective_card)
    card = CardModel(**card.dict())
    card.owner = owner
    card = update_card_by_id(card, db, id)
    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_UPDATE_CARD, db=db)
    # except: 
    #     return card
    
    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_UPDATE_CARD, db))
    log_thread.start()
    return card




def user_list_cards(owner: str, db: Session, offset: int = 0, limit: int =100, is_active: bool = False): 
    cards, total = list_card_by_owner(owner=owner,db= db,offset= offset,limit= limit, is_active=is_active)
    return cards, total


def user_get_card_by_id_and_owner(owner: str, db: Session, id: int):
    card = get_card_by_id_and_owner(id_card=id,owner=owner, db=db)
    if card is None: 
        return None
    return card 


def user_delete_card_by_id_and_owner(owner: str, db: Session, id: int):
    card = delete_card_by_id_and_owner(id_card=id,owner=owner, db=db)
    if card is None: 
        return None
    

    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_DETELE_CARD, db=db)
    # except: 
    #     return card
    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_DETELE_CARD, db))
    log_thread.start()
    return card