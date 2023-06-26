from sqlalchemy.orm import Session

from schemas.library_load_form import LibraryLoanFormModel
from schemas.helper import CustomJSONEncoder
from db.models.library_loan_form import LibraryLoanForm
import json
import uuid
from const import detail_error




def create_new_library_loan_form(form: LibraryLoanFormModel, db:Session): 
    # form_data = form.dict()  # Chuyển đổi thành từ điển
    # new_form = LibraryLoanForm(**form_data)  
    # new_form.detail_book = json.dumps(form.detail_book, cls=CustomJSONEncoder)




    existing_form = db.query(LibraryLoanForm).filter(
        LibraryLoanForm.owner == form.owner,
        LibraryLoanForm.id_card == form.id_card
    )

    if existing_form is not None: 
        raise detail_error.CODE_ENTITY_EXISTS



    form_db = LibraryLoanForm(
        created_at = form.created_at, 
        expires_at = form.expires_at, 
        id_card = form.id_card, 
        ids_books = json.dumps(form.ids_books), 
        owner = form.owner
    )
    db.add(form_db)
    db.commit()
    db.refresh(form_db)
    return form_db



def list_library_loan_form_by_owner(owner: str, db: Session):
    forms = db.query(LibraryLoanForm).filter(LibraryLoanForm.owner == owner).all()
    return forms



def get_library_load_form_by_id_and_owner(owner: str, id: str, db: Session):
    form = db.query(LibraryLoanForm).filter(
        LibraryLoanForm.owner == owner,
        LibraryLoanForm.id == id
    ).first()
    return form





