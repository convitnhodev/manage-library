from schemas.rules import RuleShow, RuleBase, RuleCreate
from db.models.rules import Rule
import json
from sqlalchemy.orm import Session
from db.repository.rules import create_rule_by_owner


def convert_rule_from_DB_to_show(rule: Rule):
    show = RuleShow(
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


def admin_create_rule(rule_create: RuleCreate, db:Session, owner: str): 
    rule = RuleBase(**rule_create.dict())
    rule.owner = owner
    rule = create_rule_by_owner(rule, db)
    return convert_rule_from_DB_to_show(rule)
