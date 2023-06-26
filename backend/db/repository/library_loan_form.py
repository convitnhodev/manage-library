from sqlalchemy.orm import Session

from schemas.library_load_form import LibraryLoanFormModel
from schemas.helper import CustomJSONEncoder
from db.models.library_loan_form import LibraryLoanForm
import json
import uuid





def create_new_library_loan_form(form: LibraryLoanFormModel, db:Session): 
    form_data = form.dict()  # Chuyển đổi thành từ điển
    new_form = LibraryLoanForm(**form_data)  
    new_form.detail_book = json.dumps(form.detail_book, cls=CustomJSONEncoder)
    db.add(new_form)
    db.commit()
    db.refresh(new_form)
    return new_form



def list_library_loan_form_by_owner(owner: str, db: Session):
    forms = db.query(LibraryLoanForm).filter(LibraryLoanForm.owner == owner).all()
    return forms



def get_library_load_form_by_id_and_owner(owner: str, id: str, db: Session):
    form = db.query(LibraryLoanForm).filter(
        LibraryLoanForm.owner == owner,
        LibraryLoanForm.id == id
    ).first()
    return form





