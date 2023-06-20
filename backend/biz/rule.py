from schemas.rules import RuleShow
from db.models.rules import Rule
import json


def ConvertRuleFromDBToShow(rule: Rule):
    show = RuleShow(
        min_age = rule.min_age,
        max_age = rule.max_age, 
        time_effective_card = rule.time_effective_card, 
        numbers_category = rule.numbers_category, 
        max_day_borrow = rule.max_day_borrow,
        distance_year = rule.distance_year,
        max_items_borrow = rule.max_items_borrow,
        detail_category = json.loads(rule.detail_category), 
        detail_type = json.loads(rule.detail_type)

    )
    return show



    # min_age: int
    # max_age: int 
    # time_effective_card: int 
    # numbers_category: int 
    # detail_category: List[str]
    # detail_type: List[str]
    # max_day_borrow: int
    # max_items_borrow: int 
    # distance_year: int 