from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.models.cards import Card

import uuid


def create_new_card(card: CardCreate, db:Session): 
    card = Card(
        id = str(uuid.uuid4()),
        name = card.name, 
        type = card.type,
        dob = card.dob, 
        address = card.address, 
        email = card.email, 
    )

    db.add(card)
    db.commit()
    db.refresh(card)
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






