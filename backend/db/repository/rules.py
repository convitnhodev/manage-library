from sqlalchemy.orm import Session
from db.models.rules import Rule
from schemas.rules import RuleCreate, RuleBase
import json

def list_rule_by_owner(owner: str, db: Session):
    rule = db.query(Rule).filter(Rule.owner == owner).all()
    return rule 

def get_rule_by_id(id: int, db: Session):
    rule = db.query(Rule).filter(Rule.id == id).first()
    return rule 



def get_rule_by_onwer_and_id(owner: str, id: int, db: Session):
    rule = db.query(Rule).filter(Rule.owner == owner, Rule.id == id).first()
    return rule 


def delete_rule_by_onwer_and_id(owner: str, id: int, db: Session):
    existing_rule = db.query(Rule).filter(Rule.owner == owner, Rule.id == id).first()
    if existing_rule: 
        db.delete(existing_rule)
        db.commit()
        return existing_rule
    
    return None


def update_rule_by_owner_and_id(owner: str, id: int, rule: RuleBase, db: Session): 

    existing_rule = db.query(Rule).filter(Rule.owner == rule.owner, Rule.id == id).first()
    if existing_rule is None:
        return None 

    if existing_rule:
        existing_rule.min_age = rule.min_age
        existing_rule.max_age = rule.max_age
        existing_rule.time_effective_card = rule.time_effective_card
        existing_rule.numbers_category = rule.numbers_category
        existing_rule.detail_category = json.dumps(rule.detail_category)
        existing_rule.max_day_borrow = rule.max_day_borrow
        existing_rule.max_items_borrow = rule.max_items_borrow
        existing_rule.created_at = rule.created_at
        existing_rule.distance_year = rule.distance_year
        db.commit()
        db.refresh(existing_rule)
        return existing_rule
    try: 
        db.query(Rule).filter(Rule.owner == owner, Rule.id == id).update(existing_rule)
        db.commit()  # Commit the changes to the database
        db.refresh(existing_rule)
        return existing_rule  # Refresh the new_rule object with the updated values from the database
    except Exception as e:
        raise e 



def update_rule_by_owner(owner: str, rule: RuleBase, db: Session): 

    existing_rule = db.query(Rule).filter(Rule.owner == rule.owner).first()
    if existing_rule is None:
        return None 

    if existing_rule:
        existing_rule.min_age = rule.min_age
        existing_rule.max_age = rule.max_age
        existing_rule.time_effective_card = rule.time_effective_card
        existing_rule.numbers_category = rule.numbers_category
        existing_rule.detail_category = json.dumps(rule.detail_category)
        existing_rule.max_day_borrow = rule.max_day_borrow
        existing_rule.max_items_borrow = rule.max_items_borrow
        existing_rule.created_at = rule.created_at
        db.commit()
        db.refresh(existing_rule)
        return existing_rule
    try: 
        db.query(Rule).filter(Rule.owner == owner, Rule.id == id).update(existing_rule)
        db.commit()  # Commit the changes to the database
        db.refresh(existing_rule)
        return existing_rule  # Refresh the new_rule object with the updated values from the database
    except Exception as e:
        raise e 


def delete_rule_by_owner(owner: str, db: Session):
    db.query(Rule).filter(Rule.owner == owner).delete()
    db.commit()


def create_rule_by_owner(rule: RuleBase, db: Session):
    existing_rule = db.query(Rule).filter(Rule.owner == rule.owner).first()

    if existing_rule:
        existing_rule.min_age = rule.min_age
        existing_rule.max_age = rule.max_age
        existing_rule.time_effective_card = rule.time_effective_card
        existing_rule.numbers_category = rule.numbers_category
        existing_rule.detail_category = json.dumps(rule.detail_category)
        existing_rule.max_day_borrow = rule.max_day_borrow
        existing_rule.max_items_borrow = rule.max_items_borrow
        existing_rule.created_at = rule.created_at
        db.commit()
        db.refresh(existing_rule)
        return existing_rule
    else:
        new_rule = Rule(
            owner=rule.owner,
            min_age=rule.min_age,
            max_age=rule.max_age,
            time_effective_card=rule.time_effective_card,
            numbers_category=rule.numbers_category,
            detail_category=json.dumps(rule.detail_category),
            detail_type = json.dumps(rule.detail_type),
            max_day_borrow=rule.max_day_borrow,
            max_items_borrow=rule.max_items_borrow,
            created_at=rule.created_at,
            distance_year = rule.distance_year
        )
        db.add(new_rule)
        db.commit()
        db.refresh(new_rule)
        return new_rule
    




    




    