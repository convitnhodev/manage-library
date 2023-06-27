from fastapi import APIRouter, Depends,HTTPException, status, Query
from sqlalchemy.orm import Session
from schemas.books import BookCreate, BaseModel
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from biz.book import user_create_books, user_list_book_by_owner, user_get_book_by_id
from biz.book import user_list_book_borrowed_by_owner
from biz.book import user_delete_book_by_id, user_update_book_by_id
from schemas.common import ListReturn
from schemas.books import DetailAddingBook

from const import detail_error 

router = APIRouter()
@router.post("/")
def create_new_book(book: BookCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    try: 
        result = user_create_books(book_create=book, db=db, owner= current_user.owner)
        return result

    except Exception as e:  
        code = detail_error.CODE_ERROR_COMOM
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    

@router.get("")
def user_list_book(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User=Depends(get_current_user_from_token)):
    books_return, total  = user_list_book_by_owner(owner=current_user.owner, db = db, offset=offset, limit=limit)
    return ListReturn(data=books_return, total=total)


@router.get("/borrow")
def user_list_book_borrowed(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User=Depends(get_current_user_from_token)):
    books_return, total  = user_list_book_borrowed_by_owner(owner=current_user.owner, db = db, offset=offset, limit=limit)
    return ListReturn(data=books_return, total=total)




@router.get("/{id}")
def user_get_book(id: int,db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    book_return = user_get_book_by_id(id=id, db=db, owner=current_user.owner)
    return book_return

@router.delete("/{id}")
def user_delete_book(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    return user_delete_book_by_id(id=id, db=db, owner=current_user.owner)



@router.put("/{id}")
def update_book(id: int, book: DetailAddingBook, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    try: 
        book = user_update_book_by_id(id=id, owner=current_user.username, book=book, db=db, updated_by=current_user.username)
        if book is not None: 
            return book 
        code = detail_error.CODE_RECORD_NOT_FOUND
        return HTTPException(status_code = code, 
                             detail = detail_error.map_err[code])
    
    except: 
        code = detail_error.CODE_CANNOT_UPDATE
        raise HTTPException(status_code = code, detail = detail_error.map_err[code])