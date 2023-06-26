from schemas.rules import RuleShow, RuleBase, RuleCreate
from db.models.rules import Rule
import json
from sqlalchemy.orm import Session
from db.repository.users import list_user_by_owner

def admin_list_users(owner: str, db: Session):
    users = list_user_by_owner(owner, db)
    return users 
