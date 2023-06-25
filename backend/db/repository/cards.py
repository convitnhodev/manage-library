from sqlalchemy.orm import Session

from schemas.cards import CardModel
from db.models.cards import Card
from datetime import datetime
from sqlalchemy import or_, and_
import uuid


def create_new_card(card: CardModel, db:Session): 
    card_data = card.dict()  # Chuyển đổi thành từ điển
    new_card = Card(**card_data)  # Sử 
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return card


def update_card_by_id(card: CardModel, db:Session, id: int): 
    existing_card = db.query(Card).filter(Card.owner == card.owner, Card.id == id).first()
    if existing_card is None:
        return None 
    
    existing_card.address = card.address
    existing_card.dob = card.dob
    existing_card.email = card.email
    existing_card.name = card.name
    existing_card.type = card.type
    

    db.commit()
    db.refresh(existing_card)
    return existing_card



def get_card_by_name(name_card: str, db: Session):
    card = db.query(Card).filter(Card.name == name_card).first()
    return card


def get_card_by_id_and_owner(id_card: int, owner: str,  db: Session):
    card = db.query(Card).filter(Card.id == id_card, Card.owner == owner).first()
    return card



def delete_card_by_id_and_owner(id_card: int, owner: str, db: Session):
    existing_card = db.query(Card).filter(Card.owner == owner, Card.id == id_card).first()
    if existing_card: 
        db.delete(existing_card)
        db.commit()
        return existing_card
    
    return None


def list_cards_by_type_card(card_type: str, db: Session):
    cards = db.query(Card).filter(Card.type == card_type).all()
    return cards


def get_card_by_owner(owner: str, db: Session):
    card = db.query(Card).filter(Card.owner == owner).first()
    return card


def list_card_by_owner(owner: str, db: Session, offset: int , limit: int, is_active: bool):
    if not is_active :
        cards  = db.query(Card).filter(Card.owner == owner).offset(offset).limit(limit).all()
        return cards
    current_time = datetime.now()
    condition = or_(Card.expires_at > current_time, Card.expires_at.is_(None))
    cards = db.query(Card).filter(and_(Card.owner == owner, condition)).offset(offset).limit(limit).all()
    return cards




