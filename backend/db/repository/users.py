from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher



def create_new_user(user: UserCreate, db:Session): 
    user = User (
        name = user.name,
        username = user.username, 
        numberphone = user.numberphone, 
        dob = user.dob,
        address = user.address,
        email = user.email,
        password = Hasher.get_password_hash(user.password),
        is_active = True,
        is_supperuser = False,
        owner = "1"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user




