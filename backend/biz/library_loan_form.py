from schemas.library_load_form import LibraryLoanFormModel, LibraryLoanFormCreate
from db.models.library_loan_form import LibraryLoanForm
import json
from sqlalchemy.orm import Session
from db.repository.library_loan_form import create_new_library_loan_form
from db.repository.library_loan_form import list_library_loan_form_by_owner
from schemas.helper import object_as_dict



def create_library_loan_form(form_create: LibraryLoanFormCreate, db:Session, owner: str): 
    form = LibraryLoanFormModel(**form_create.dict())
    form.owner = owner
    form  = create_new_library_loan_form(form, db)
    data_form = object_as_dict(form)
    form_return = LibraryLoanForm(**data_form)
    form_return.detail_book = json.loads(form.detail_book)
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