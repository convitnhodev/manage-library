from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.users import UserCreate, UserShow
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from db.repository.users import create_new_user


router = APIRouter()

@router.post("/register", response_model=UserShow)
def create_user(user: UserCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    user = create_new_user(user, db, current_user.owner)
    return user