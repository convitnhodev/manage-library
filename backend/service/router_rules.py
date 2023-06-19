from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from schemas.rules import RuleCreate
from db.session import get_db
from db.models.users import User
from service.router_login import get_current_user_from_token
from db.repository.rules import get_role_by_owner, create_rule_by_owner

router = APIRouter()
@router.post("/new")
def create_new_rule(rule: RuleCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="You dont have permission")
    if current_user.username != current_user.owner :
        raise credentials_exception
    
    rule = create_rule_by_owner(rule= rule, db = db, owner=current_user.username)
    return rule


@router.get("/get")
def get_rule(db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    
    empty_exception = HTTPException(status_code=HTTP_204_NO_CONTENT,
                                          detail="Rule empty")

    rule = get_role_by_owner(db = db, owner=current_user.owner)
    if rule is None:
        raise empty_exception
    return rule




