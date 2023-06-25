from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.session import get_db

from db.repository.cards import create_new_card, get_card_by_id, get_card_by_name
from db.repository.cards import list_cards_by_type_card

from router.router_login import get_current_user_from_token
from db.models.users import User
from biz.card import is_card_valid, user_create_new_card


from const import detail_error 


router = APIRouter()

@router.post("")
def create_card(card: CardCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    try:  
        result = user_create_new_card(card, db, current_user.owner)
        if type(result) == type(detail_error.CODE_VALID): 
            return HTTPException(status_code = result, 
                                detail = detail_error.map_err[result])
        return result
    except Exception as e:  
        raise HTTPException(status_code = 500, 
                            detail = str(e))


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

