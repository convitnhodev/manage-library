from sqlalchemy.orm import Session
from db.models.rules import Rule
from schemas.rules import RuleCreate
import json
import uuid

def get_rule_by_owner(owner: str, db: Session):
    rule = db.query(Rule).filter(Rule.owner == owner).first()
    return rule 

def get_rule_by_id(id: str, db: Session):
    rule = db.query(Rule).filter(Rule.id == id).first()
    return rule 


def delete_rule_by_owner(owner: str, db: Session):
    db.query(Rule).filter(Rule.owner == owner).delete()
    db.commit()


def create_rule_by_owner(owner: str, rule: RuleCreate, db: Session):
    existing_rule = db.query(Rule).filter(Rule.owner == owner).first()

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
            id=str(uuid.uuid4()),
            owner=owner,
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
    




    




    