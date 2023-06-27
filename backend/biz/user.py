from schemas.rules import RuleShow, RuleBase, RuleCreate
from db.models.rules import Rule
import json
from sqlalchemy.orm import Session
from db.repository.users import list_user_by_owner, delete_user
from const import detail_error

def admin_list_users(owner: str, db: Session):
    users = list_user_by_owner(owner, db)
    return users 


def admin_delete_user(owner: str, db: Session, id: int):
    result = delete_user(id=id, db=db, owner=owner)
    if not result: 
        raise detail_error
    return True
