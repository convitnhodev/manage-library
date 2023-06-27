from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.users import UserCreate, UserShow
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from db.repository.users import create_new_user
from authrization.iam import authrization
from const import resource, detail_error
from biz.user import admin_list_users
from biz.rule import user_create_rule
from schemas.rules import RuleCreate
from datetime import datetime
from const import default
from db.repository import logs 

router = APIRouter()

@router.post("/registration", response_model=UserShow)
def create_user(user: UserCreate, db: Session= Depends(get_db), current_user:
                 User=Depends(get_current_user_from_token)):
    
    if not current_user.is_supperuser : 
        code = detail_error.CODE_UNAUTHORIZED
        raise HTTPException(status_code =  code ,
                            detail = detail_error.map_err[code]) 
    try: 
        user = create_new_user(user, db, owner=current_user.username, is_admin=False)
        return user 
    except Exception as e: 
        return e 
    


@router.post("/admin/registration", response_model=UserShow)
def create_user(user: UserCreate, db: Session= Depends(get_db)):
    
    if authrization.enforce(user.username, resource.RESOUCE_REGISTRATION, resource.ACTION_WRITE):
        try: 
            user = create_new_user(user, db, owner=user.username, is_admin=True)
            rule_default = RuleCreate(
                min_age = default.MIN_AGE, 
                max_age = default.MAX_AGE, 
                time_effective_card = default.TIME_EXPIRATION_CARD, 
                detail_type = default.DETAIL_TYPE, 
                detail_category = default.DETAIL_CATEGORY, 
                numbers_category = len(default.DETAIL_CATEGORY), 
                max_day_borrow = default.DAY_BORROW, 
                max_items_borrow = default.MAX_ITEMS_BORROW, 
                distance_year = default.DISTANCE_YEAR,
            )

            user_create_rule(rule_create=rule_default, db=db, owner=user.username)

            



            return user
        except Exception as e: 
            code = detail_error.CODE_USER_EXISTS
            raise HTTPException(status_code=code, 
                                detail= detail_error.map_err[code])
        
    code = detail_error.CODE_UNAUTHORIZED 
    raise HTTPException(status_code = code,
                        detail=detail_error.map_err[code])


@router.get("/admin/users")
def list_users(db:  Session=Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    if not current_user.is_supperuser : 
        code = detail_error.CODE_UNAUTHORIZED
        raise HTTPException(status_code =  code ,
                            detail = detail_error.map_err[code]) 
  
    users = admin_list_users(db=db, owner=current_user.owner)
    return users

@router.get("/admin/logs") 
def list_log(action: str = None, start: datetime = None, end: datetime = None,db: Session=Depends(get_db),current_user: User=Depends(get_current_user_from_token)):
    return logs.list_log(owner=current_user.owner, start_time=start, end_time=end, action=action, db=db)
