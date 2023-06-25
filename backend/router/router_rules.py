from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from schemas.rules import RuleCreate, RuleShow
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from db.repository.rules import get_rule_by_owner, create_rule_by_owner
from biz.rule import admin_create_rule

router = APIRouter()
@router.post("/new")
def create_new_rule(rule: RuleCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="You dont have permission")
    # authrization
    if current_user.username != current_user.owner :
        raise credentials_exception
    
    rule = admin_create_rule(rule_create= rule, db = db, owner=current_user.username)
    return rule




@router.get("/get")
def get_rule(db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    
    empty_exception = HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                          detail="Rule empty")

    rule = get_rule_by_owner(db = db, owner=current_user.owner)
    if rule is None:
        raise empty_exception
    rule_show = ConvertRuleFromDBToShow(rule=rule)
    return rule_show




