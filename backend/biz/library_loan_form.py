from schemas.library_load_form import LibraryLoanFormModel, LibraryLoanFormCreate
from db.models.library_loan_form import LibraryLoanForm
import json
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from db.repository.library_loan_form import create_new_library_loan_form
from db.repository.library_loan_form import list_library_loan_form_by_owner
from db.repository.books import  get_book_by_id
from schemas.helper import object_as_dict
from db.repository.books import update_book_amount_borrowed
from db.repository.rules import list_rule_by_owner
from const import detail_error, default

def check_number_of_book(book_id:int, number: int, db:Session, owner: str): 
    book = get_book_by_id(id=book_id, owner=owner, db=db)
    if book.amount_borrowed + number > book.numbers: 
        return False
    return True

def borrow_book_by_id(book_id: int, number: int, db: Session, owner: str):
    book = update_book_amount_borrowed(id=book_id, amount=number, owner=owner, db=db)
    return book

def delete_library_loan_form(form_delete: LibraryLoanFormCreate, db: Session, owner=str):
    form = LibraryLoanFormModel (
        owner = owner, 
        id_card = form_delete.id_card, 
        ids_books = form_delete.ids_books
    )

    rules = list_rule_by_owner(owner, db)
    if len(rules) == 0 : 
        rule == None
    else: 
        rule = rules[0]

    

    for book_id in form.ids_books: 
        borrow_book_by_id(book_id= book_id, number=1, db=db, owner=owner)




    


def create_library_loan_form(form_create: LibraryLoanFormCreate, db:Session, owner: str): 
    form = LibraryLoanFormModel (
        owner = owner, 
        id_card = form_create.id_card, 
        ids_books = form_create.ids_books
    )

    rules = list_rule_by_owner(owner, db)
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

    try:
        form_created  = create_new_library_loan_form(form, db)
    except Exception as e: 
        raise detail_error.CODE_CANNOT_CREATE
        

    for book_id in form.ids_books: 
        borrow_book_by_id(book_id= book_id, number=1, db=db, owner=owner)
    data_form = object_as_dict(form_created)
    form_return = LibraryLoanForm(**data_form)
    form_return.ids_books = json.loads(form.ids_books)
    return form_return


def user_list_library_loan_form_by_owner(owner: str, db: Session):
    forms = list_library_loan_form_by_owner(owner, db)
    models_forms = []
    for form in forms:
        data_form = object_as_dict(form)
        model_form = LibraryLoanForm(**data_form)
        model_form.detail_book = json.loads(form.detail_book)
        models_forms.append(model_form)
    return models_forms