from schemas.rules import RuleShow, RuleBase, RuleCreate
from db.models.rules import Rule
import json
from sqlalchemy.orm import Session
from db.repository.rules import create_rule_by_owner
from db.repository.rules import get_rule_by_onwer_and_id
from db.repository.rules import delete_rule_by_onwer_and_id
from db.repository.rules import update_rule_by_owner_and_id, update_rule_by_owner
from db.repository.rules import list_rule_by_owner
from db.repository.logs import create_log
import threading
from biz.log import log_task
from const import default
def convert_rule_from_DB_to_show(rule: Rule):
    show = RuleShow(
        id = rule.id,
        min_age = rule.min_age,
        max_age = rule.max_age, 
        time_effective_card = rule.time_effective_card, 
        numbers_category = rule.numbers_category, 
        max_day_borrow = rule.max_day_borrow,
        distance_year = rule.distance_year,
        max_items_borrow = rule.max_items_borrow,
        detail_category = json.loads(rule.detail_category), 
        detail_type = json.loads(rule.detail_type), 
        owner = rule.owner
    )
    return show


def user_create_rule(rule_create: RuleCreate, db:Session, owner: str): 
    rule = RuleBase(**rule_create.dict())
    rule.owner = owner
    rule = create_rule_by_owner(rule, db)
    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_CREATE_RULE, db=db)
    # except:

     
    #     return convert_rule_from_DB_to_show(rule)
    
    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_CREATE_RULE, db))
    log_thread.start()
    return convert_rule_from_DB_to_show(rule)


def user_get_rule_by_id(owner: str, id: int, db:Session):
    rule = get_rule_by_onwer_and_id(owner, id, db)
    if rule is None: 
        return None
    rule_show = convert_rule_from_DB_to_show(rule)
    return rule_show


def user_list_rule(owner: str, db:Session): 
    rules = list_rule_by_owner(owner, db)
    rule_shows = []
    for rule in rules:
        rule_show = convert_rule_from_DB_to_show(rule)
        rule_shows.append(rule_show)
    return rule_shows 


def user_delete_rule_by_id(owner: str, id: int, db: Session): 
    rule = delete_rule_by_onwer_and_id(owner, id, db)
    if rule is None: 
        return None 
    rule_show = convert_rule_from_DB_to_show(rule)
    # try:
    #     create_log(owner=owner, db=db, action=default.ACTION_DELETE_RULE, actor=owner)
    # except: 
    #     return rule_show
    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_DELETE_RULE, db))
    log_thread.start()
    return rule_show



def user_update_rule_by_id(owner: str, id: int, rule_update: RuleCreate, db: Session): 
    rule = RuleBase(**rule_update.dict())
    rule.owner = owner
    try: 
        rule = update_rule_by_owner_and_id(owner=owner, id = id, rule = rule, db = db)
        if rule is None: 
            return None
        

        # try:
        #     create_log(owner=owner, db=db, action=default.ACTION_UPDATE_RULE, actor=owner)
        # except: 
        #     return convert_rule_from_DB_to_show(rule)
        log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_UPDATE_RULE, db))
        log_thread.start()
        return convert_rule_from_DB_to_show(rule)
    except Exception as e:
        raise e 

   


def user_update_rule_belong(owner: str, rule_update: RuleCreate, db: Session): 
    rule = RuleBase(**rule_update.dict())
    rule.owner = owner
    try: 
        rule = update_rule_by_owner(owner=owner, rule = rule, db = db)
        if rule is None: 
            return None
        

        # try:
        #     create_log(owner=owner, db=db, action=default.ACTION_UPDATE_RULE, actor=owner)
        # except: 
        #     return convert_rule_from_DB_to_show(rule)
        log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_UPDATE_RULE, db))
        log_thread.start()
        return convert_rule_from_DB_to_show(rule)
    except Exception as e:
        raise e 

   