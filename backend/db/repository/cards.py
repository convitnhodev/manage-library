from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.models.cards import Card



def create_new_card(card: CardCreate, db:Session): 
    card = Card(
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




