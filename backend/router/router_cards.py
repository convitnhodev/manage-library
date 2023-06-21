from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.session import get_db

from db.repository.cards import create_new_card, get_card_by_id, get_card_by_name
from db.repository.cards import list_cards_by_type_card

from router.router_login import get_current_user_from_token
from db.models.users import User
from biz.card import is_card_valid


from const import detail_error as err


router = APIRouter()

@router.post("/new")
def create_card(card: CardCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    try: 
        code = is_card_valid(card=card, db=db, owner=current_user.owner)
        if code != err.CODE_VALID:
            err_return = HTTPException(status_code= code ,
                                  detail= err.map_err[code])
            raise err_return
        card = create_new_card(card, db)
    except :
        raise err_return
    return card


@router.get("/{id}")
def get_card_by_id_api(id: str, db: Session = Depends(get_db)):
    card = get_card_by_id(id_card=id, db=db)
    if not card:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return card




@router.get("/{name_card}")
def get_card_by_name_api(name_card: str, db: Session = Depends(get_db)):
    print(name_card)
    card = get_card_by_name(name_card=name_card, db=db)
    if not card:
        return  HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return card


@router.get("{card_type}")
def list_cards_by_type_api(card_type: str, db: Session = Depends(get_db)):
    cards = list_cards_by_type_card(card_type=card_type, db=db)
    if not cards:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return cards

