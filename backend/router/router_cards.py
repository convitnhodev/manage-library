from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session


from schemas.common import ListReturn
from schemas.cards import CardCreate
from db.session import get_db


from biz.card import user_get_card_by_id_and_owner
from biz.card import user_delete_card_by_id_and_owner

from router.router_login import get_current_user_from_token
from db.models.users import User
from biz.card import is_card_valid, user_create_new_card, user_list_cards
from biz.card import user_update_card


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
        code = detail_error.CODE_ERROR_COMOM
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])


@router.get("/{id}")
def get_card_by_id(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    card = user_get_card_by_id_and_owner(id=id, db=db, owner=current_user.owner)
    if card == None: 
        code = detail_error.CODE_RECORD_NOT_FOUND
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    
    return card


@router.delete("/{id}")
def delete_card_by_id(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    card = user_delete_card_by_id_and_owner(id=id, db=db, owner=current_user.owner)
    if card == None: 
        code = detail_error.CODE_RECORD_NOT_FOUND
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    
    return card


@router.put("/{id}")
def update_card(id: int, card: CardCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    try:
        card = user_update_card(card=card, db=db, owner=current_user.owner, id=id)
        if card is not None:
            return card
        code = detail_error.CODE_RECORD_NOT_FOUND
        return  HTTPException(status_code=code, 
                            detail = detail_error.map_err[code])
    except: 
        code = detail_error.CODE_CANNOT_UPDATE
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    



@router.get("")
def list_cards(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    is_active: bool = False, 
    db: Session = Depends(get_db),
    current_user: User=Depends(get_current_user_from_token)):
    cards_return, total = user_list_cards(owner=current_user.owner, db=db, offset=offset, limit=limit, is_active=is_active)

    return ListReturn(data=cards_return, total=total)
