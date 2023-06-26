from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from schemas.library_load_form import LibraryLoanFormModel, LibraryLoanFormCreate
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from db.repository.rules import create_rule_by_owner
from biz.library_loan_form import create_library_loan_form,user_list_library_loan_form_by_owner 
from biz.library_loan_form import check_number_of_book,user_get_librara_by_owner_and_id 

from const import detail_error 

router = APIRouter()
@router.post("")
def create_new_library_loan_form(form: LibraryLoanFormCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
   
    try:
        form_return = create_library_loan_form(form_create=form, db=db, owner= current_user.owner)
        return form_return
    except: 
        code = detail_error.CODE_CANNOT_CREATE
        raise HTTPException(status_code = code ,
                            detail = detail_error.map_err[code])
   

@router.get("")
def list_library_loan_forms(db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    form_return = user_list_library_loan_form_by_owner(owner=current_user.owner, db = db)
    return form_return

@router.get("/{id}")
def get_library_loan_form_by_id(
    id: int,
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user_from_token)):

    form = user_get_librara_by_owner_and_id(owner=current_user.owner, id = id, db= db)
    if form is None:
        code = detail_error.CODE_RECORD_NOT_FOUND
        raise HTTPException(status_code = code , 
                            detail_error = detail_error.map_err[code])
    
    return form 


@router.get("/book/{id}")
def check_book_by_id(id: int, db: Session = Depends(get_db),current_user: User=Depends(get_current_user_from_token)):
    if check_number_of_book(id, 1, db, current_user.owner): 
        return True
    return False

