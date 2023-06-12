from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.session import get_db

from db.repository.cards import create_new_card


router = APIRouter()

@router.post("/new")
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    card = create_new_card(card, db)
    return card 

