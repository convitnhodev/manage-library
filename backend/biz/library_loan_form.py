from schemas.library_load_form import LibraryLoanFormModel, LibraryLoanFormCreate
from db.models.library_loan_form import LibraryLoanForm
import json
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from db.repository.library_loan_form import create_new_library_loan_form
from db.repository.library_loan_form import get_library_load_form_by_id_and_owner
from db.repository.library_loan_form import list_library_loan_form_by_owner
from db.repository.library_loan_form import delete_library_loan_form
from db.repository.books import get_books_by_ids
from db.repository.books import  get_book_by_id
from schemas.helper import object_as_dict
from db.repository.books import update_book_amount_borrowed, update_books_amount_borrowed
from db.repository.rules import list_rule_by_owner
from const import detail_error, default
from db.repository.logs import create_log
import threading
from biz.log import log_task

def check_number_of_book(book_id:int, number: int, db:Session, owner: str): 
    book = get_book_by_id(id=book_id, owner=owner, db=db)
    if book.amount_borrowed + number > book.numbers: 
        return False
    return True

def borrow_book_by_id(book_id: int, number: int, db: Session, owner: str):
    book = update_book_amount_borrowed(id=book_id, amount=number, owner=owner, db=db)
    if number > 0:
        action = default.ACTION_BORROW_BOOK
    else:
        action = default.ACTION_RETURN_BOOK
    
    log_thread = threading.Thread(target=log_task, args=(owner, book_id, action, db))
    log_thread.start()
    return book



# adding 
def borrow_books(book_id: list[int], number: int, db: Session, owner: str, date_return: date, date_must_return: date): 
    if number > 0 : 
        books = update_books_amount_borrowed(ids=book_id, db=db, owner=owner, amount=number, date_must_return=date_must_return, date_return=date_return, is_return=False)
        return books 
    
    return update_books_amount_borrowed(ids=book_id, db=db, owner=owner, amount=number, date_must_return=date_must_return, date_return=date_return, is_return=True)






def user_delete_library_loan_form(id: int, db: Session, owner=str):
    # try:
    #     form  = delete_library_loan_form(id=id, owner = owner, db = db)
    # except Exception as e: 
    #     raise detail_error.CODE_CANNOT_DELETE
    
    # list_id_book = json.loads(form.ids_books)
    # for book_id in list_id_book: 
    #     borrow_book_by_id(book_id= book_id, number=-1, db=db, owner=owner)


    #adding 

    try: 
        if not db.is_active:  # Check if a transaction is already in progress
            # Begin the transaction
            db.begin()

        try:
            form = delete_library_loan_form(id=id, owner = owner, db = db)
        except Exception as e: 
            raise detail_error.DETAIL_CANNOT_DELETE
        

        list_id_book = json.loads(form.ids_books)
        
        borrow_books(book_id=list_id_book, number= -1, db=db, owner=owner, date_must_return=None, date_return=datetime.now())
            

        # for book_id in form.ids_books: 
        #     borrow_book_by_id(book_id= book_id, number=1, db=db, owner=owner)

    
    except Exception as e:
        print(e)
        db.rollback()
        raise detail_error.CODE_CANNOT_CREATE



    #end adding 



    data_form = object_as_dict(form)
    form_return = LibraryLoanForm(**data_form)
    form_return.ids_books = json.loads(form.ids_books)

    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_DETELE_LIBRARY_FORM, db=db)
    # except: 
    #     return form_return
    

    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_DETELE_LIBRARY_FORM, db))
    log_thread.start()

    return form_return





    


def create_library_loan_form(form_create: LibraryLoanFormCreate, db:Session, owner: str): 
    form = LibraryLoanFormModel (
        owner = owner, 
        id_card = form_create.id_card, 
        ids_books = form_create.ids_books
    )

    try: 
        rules = list_rule_by_owner(owner, db)
    except: 
        raise detail_error.CODE_CANNOT_CREATE
    if len(rules) == 0:
        rule = None
    else :
        rule = rules[0]
        
        
    if rule is not None and rule.max_items_borrow < len(form.ids_books):
        return detail_error.CODE_INVALID_NUMBER_BOOKS_CAN_BE_BORROW
    if rule is None: 
        max_day_borrow =default.DAY_BORROW 
    else :
        max_day_borrow = rule.max_day_borrow
    expire = form_create.created_at + timedelta(days=max_day_borrow)
    form.expires_at = expire

    books = get_books_by_ids(ids = form_create.ids_books, owner = owner, db = db)
    if len(books) != len(form_create.ids_books):
        raise detail_error.CODE_CANNOT_CREATE
    

    # check valid of book 
    for book in books:
        if book.numbers <= book.amount_borrowed:
            raise detail_error.CODE_CANNOT_CREATE
        
    
    try: 
        if not db.is_active:  # Check if a transaction is already in progress
            # Begin the transaction
            db.begin()

        try:
            form_created  = create_new_library_loan_form(form, db)
        except Exception as e: 
            raise detail_error.CODE_CANNOT_CREATE
        
        borrow_books(book_id=form.ids_books, number=1, db=db, owner=owner, date_must_return=expire, date_return=datetime.now())
            

        # for book_id in form.ids_books: 
        #     borrow_book_by_id(book_id= book_id, number=1, db=db, owner=owner)

        data_form = object_as_dict(form_created)
        form_return = LibraryLoanForm(**data_form)
        form_return.ids_books = json.loads(form_created.ids_books)
    except Exception as e:
        print(e)
        db.rollback()
        raise detail_error.CODE_CANNOT_CREATE


    # try: 
    #     create_log(owner=owner, 
    #                actor=owner, action=default.ACTION_CREATE_LIBRARY_FORM, db=db)
    # except: 
    #     return form_return
    

    log_thread = threading.Thread(target=log_task, args=(owner, owner, default.ACTION_CREATE_LIBRARY_FORM, db))
    log_thread.start()
    return form_return


def user_list_library_loan_form_by_owner(owner: str, db: Session):
    forms = list_library_loan_form_by_owner(owner, db)
    forms_return = []
    for form in forms:
        data_form = object_as_dict(form)
        form_return = LibraryLoanForm(**data_form)
        form_return.ids_books = json.loads(form.ids_books)
        forms_return.append(form_return)
    return forms_return


def user_get_librara_by_owner_and_id(owner: str, id: int, db: Session):
    form = get_library_load_form_by_id_and_owner(owner=owner, id=id, db=db)
    data_form = object_as_dict(form)
    form_return = LibraryLoanForm(**data_form)
    form_return.ids_books = json.loads(form.ids_books)

    return form_return
    