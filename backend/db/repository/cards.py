from sqlalchemy.orm import Session

from schemas.cards import CardModel
from db.models.cards import Card

import uuid


def create_new_card(card: CardModel, db:Session): 
    card_data = card.dict()  # Chuyển đổi thành từ điển
    new_card = Card(**card_data)  # Sử 
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return card


def get_card_by_name(name_card: str, db: Session):
    card = db.query(Card).filter(Card.name == name_card).first()
    return card


def get_card_by_id(id_card: str, db: Session):
    card = db.query(Card).filter(Card.id == id_card).first()
    return card



def list_cards_by_type_card(card_type: str, db: Session):
    cards = db.query(Card).filter(Card.type == card_type).all()
    return cards


def get_card_by_owner(owner: str, db: Session):
    card = db.query(Card).filter(Card.owner == owner).first()
    return card







