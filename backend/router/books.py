from fastapi import APIRouter, Depends,HTTPException, status, Query
from sqlalchemy.orm import Session
from schemas.books import BookCreate, BaseModel
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from biz.book import user_create_books, user_list_book_by_owner, user_get_book_by_id
from biz.book import user_delete_book_by_id

router = APIRouter()
@router.post("/")
def create_new_book(book: BookCreate, db: Session= Depends(get_db)):
   
    book_return = user_create_books(book_create=book, db=db, owner= "haha")
    return book_return


@router.get("")
def user_list_book(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    books_return = user_list_book_by_owner(owner="haha", db = db, offset=offset, limit=limit)
    return books_return


@router.get("/{id}")
def user_get_book(id: int,db: Session = Depends(get_db)):
    book_return = user_get_book_by_id(id=id, db=db, owner="haha")
    return book_return

@router.delete("/{id}")
def user_delete_book(id: int, db: Session = Depends(get_db)): 
    return user_delete_book_by_id(id=id, db=db, owner="haha")