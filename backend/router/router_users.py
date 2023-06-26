from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.users import UserCreate, UserShow
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from db.repository.users import create_new_user
from authrization.iam import authrization
from const import resource, detail_error


router = APIRouter()

@router.post("/registration", response_model=UserShow)
def create_user(user: UserCreate, db: Session= Depends(get_db), current_user:
                 User=Depends(get_current_user_from_token)):
    
    if authrization.enforce(current_user.username, resource.RESOUCE_REGISTRATION, resource.ACTION_WRITE):
        try: 
            user = create_new_user(user, db, owner=user.username, is_admin=True)
            return user 
        except Exception as e: 
            return e 
    


@router.post("/admin/registration", response_model=UserShow)
def create_user(user: UserCreate, db: Session= Depends(get_db)):
    
    if authrization.enforce(user.username, resource.RESOUCE_REGISTRATION, resource.ACTION_WRITE):
        try: 
            user = create_new_user(user, db, owner=user.username, is_admin=True)
            return user
        except Exception as e: 
            code = detail_error.CODE_USER_EXISTS
            raise HTTPException(status_code=code, 
                                detail= detail_error.map_err[code])
        
    code = detail_error.CODE_UNAUTHORIZED 
    raise HTTPException(status_code = code,
                        detail=detail_error.map_err[code])

    