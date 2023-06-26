from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher

def list_user_by_owner(owner: str, db: Session):
    users = db.query(User).filter(User.owner == owner).all()
    return users

def create_new_user(user: UserCreate, db:Session, owner: str, is_admin: bool):
     
    user = User (
        name = user.name,
        username = user.username, 
        numberphone = user.numberphone, 
        dob = user.dob,
        address = user.address,
        email = user.email,
        password = Hasher.get_password_hash(user.password),
        is_active = True,
        is_supperuser = is_admin,
        owner = owner, 
        created_by = owner
    )
    try: 
        db.add(user)
        db.commit()
        db.refresh(user)
        return user 
    except Exception as e:
        raise e 