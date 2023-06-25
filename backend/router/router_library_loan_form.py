from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from schemas.library_load_form import LibraryLoanFormModel, LibraryLoanFormCreate
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from db.repository.rules import get_rule_by_owner, create_rule_by_owner
from biz.library_loan_form import create_library_loan_form,user_list_library_loan_form_by_owner 

router = APIRouter()
@router.post("/new")
def create_new_library_loan_form(form: LibraryLoanFormCreate, db: Session= Depends(get_db)):
   
    form_return = create_library_loan_form(form_create=form, db=db, owner= "haha")
    return form_return


@router.get("")
def list_library_loan_forms(db: Session= Depends(get_db)):
    form_return = user_list_library_loan_form_by_owner(owner="haha", db = db)
    return form_return

@router.get("/{id}")
def get_library_loan_form_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    return "a"