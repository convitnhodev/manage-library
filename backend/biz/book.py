from schemas.books import BookCreate, BookModel
from db.models.books import Book
import json
from sqlalchemy.orm import Session
from db.repository.books import add_book
from db.repository.books import list_books_by_owner
from db.repository.books import get_book_by_id
from db.repository.books import delete_book_by_id
from schemas.helper import object_as_dict



def user_create_books(book_create: BookCreate, db:Session, owner: str):
    result_added_book = []
    for book in book_create.detail_adding_book: 
        book.owner = owner
        book_added = add_book(book, db)
        result_added_book.append(book_added)

    return result_added_book

    # book = BookModel(**book_create.dict())
    # book.owner = owner
    # book  = create_new_book(book, db)
    # book_form = object_as_dict(book)
    # book_return = Book(**book_form)
    # book_return.detail_adding_book = json.loads(book.detail_adding_book)
    # return book_return


def user_list_book_by_owner(owner: str, db: Session,offset: int = 0, limit: int = 100):
    books = list_books_by_owner(owner = owner, db = db, offset = offset,limit = limit)
    # data_book = object_as_dict(books)
    # model_book = Book(**data_book)
    # model_book.detail_adding_book = json.loads(book)
    return books


def user_get_book_by_id(owner:str, id: str, db: Session) : 
    book = get_book_by_id(owner=owner, id=id, db = db)
    return book


def user_delete_book_by_id(owner:str, id: str, db: Session) : 
    book = delete_book_by_id(owner=owner, id=id, db = db)
    return book