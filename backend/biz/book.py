from schemas.books import BookCreate, BookModel, DetailAddingBook
from db.models.books import Book
from db.models.rules import Rule
import json
from sqlalchemy.orm import Session
from db.repository.books import add_book
from db.repository.books import list_books_by_owner, list_books_borred_by_owner
from db.repository.books import get_book_by_id
from db.repository.books import delete_book_by_id
from db.repository.rules import list_rule_by_owner
from db.repository.books import update_book_by_id
from db.repository.books import list_book_borrow
from schemas.helper import object_as_dict
from const import detail_error 
from datetime import date, datetime, timedelta
from const import default
from db.repository.logs import create_log
import threading
from biz.log import log_task

def is_book_valid(book: DetailAddingBook, rule: Rule):
    if rule is None: 
        return detail_error.CODE_VALID
    today = date.today()
    if today.year - book.year_of_publication > rule.distance_year: 
        return detail_error.DETAIL_INVALID_YEAR_PUBLICATION
    
    if book.category not in json.loads(rule.detail_category): 
        return detail_error.CODE_INVALID_CATEGORY_BOOK
    return detail_error.CODE_VALID


def user_create_books(book_create: BookCreate, db:Session, owner: str):
    rules = list_rule_by_owner(owner, db)
    if len(rules) == 0:
        rule = None
    else :
        rule = rules[0]

    result_check = []
    for book in book_create.detail_adding_book: 
        result = is_book_valid(book, rule)
        result_check.append(result)
        
    for check in result_check: 
        if check != detail_error.CODE_VALID: 
            raise result_check
    

    # add after checking 
    result_added_book = []
    
    for book in book_create.detail_adding_book: 
        book.owner = owner
        book_added = add_book(book, db)
        result_added_book.append(book_added)

    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_CREATE_BOOk, db=db)
    # except: 
    #     return result_added_book

    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_CREATE_BOOk, db))
    log_thread.start()

    return result_added_book

    # book = BookModel(**book_create.dict())
    # book.owner = owner
    # book  = create_new_book(book, db)
    # book_form = object_as_dict(book)
    # book_return = Book(**book_form)
    # book_return.detail_adding_book = json.loads(book.detail_adding_book)
    # return book_return


def user_list_book_by_owner(owner: str, db: Session,offset: int = 0, limit: int = 100):
    books, total  = list_books_by_owner(owner = owner, db = db, offset = offset,limit = limit)
    # data_book = object_as_dict(books)
    # model_book = Book(**data_book)
    # model_book.detail_adding_book = json.loads(book)
    return books, total 


def user_list_book_borrow(owner: str, db: Session,start_time: datetime = None, end_time: datetime = None):
    return list_book_borrow(owner=owner, db=db, start_time=start_time, end_time=end_time)

def user_list_book_borrowed_by_owner(owner: str, db: Session,offset: int = 0, limit: int = 100):
    books, total  = list_books_borred_by_owner(owner = owner, db = db, offset = offset,limit = limit)
    # data_book = object_as_dict(books)
    # model_book = Book(**data_book)
    # model_book.detail_adding_book = json.loads(book)
    return books, total 


def user_get_book_by_id(owner:str, id: str, db: Session) : 
    book = get_book_by_id(owner=owner, id=id, db = db)
    return book


def user_delete_book_by_id(owner:str, id: str, db: Session) : 
    book = delete_book_by_id(owner=owner, id=id, db = db)
    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_DELETE_BOOK, db=db)
    # except: 
    #     return book
    
    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_DELETE_BOOK, db))
    log_thread.start()
    return book


def user_update_book_by_id(owner:str, id: str, db: Session, book: DetailAddingBook, updated_by: str):
    rules = list_rule_by_owner(owner, db)
    if len(rules) == 0:
        rule = None
    else :
        rule = rules[0]

    is_valid = is_book_valid(book=book, rule=rule)
    if is_valid != detail_error.CODE_VALID: 
        return is_valid
    
    book.owner = owner
    book = update_book_by_id(id=id, db=db, book=book, updated_by=updated_by)
    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_UPDATE_BOOk, db=db)
    # except: 
    #     return book
    
    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_UPDATE_BOOk, db))
    log_thread.start()
    return book 
    
